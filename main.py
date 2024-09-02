# InstaNinja
import tkinter as tk
from tkinter import messagebox
from instagrapi import Client
import json
import threading
import time

# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)
accounts = config['accounts']

cl = Client()
current_account_index = 0

def switch_account():
    global cl, current_account_index
    if current_account_index < len(accounts):
        account = accounts[current_account_index]
        cl.logout()  # Ensure the client is logged out before switching
        if 'proxy' in account and account['proxy']:
            cl.set_proxy(account['proxy'])
        current_account_index += 1
        return account
    else:
        return None

def perform_action(action_func, action_label):
    account = switch_account()
    if not account:
        messagebox.showinfo("Info", "All actions completed for all accounts.")
        return
    
    username = account['username']
    password = account['password']
    
    # Show current account
    label_current_account.config(text=f"Current Account: {username}")
    
    # Show processing overlay
    show_processing_overlay()

    def wrapper():
        try:
            cl.login(username, password)
            action_func()
        except Exception as e:
            messagebox.showerror("Error", f"Failed for account {username}: {e}")
        finally:
            hide_processing_overlay()
            if current_account_index < len(accounts):
                label_current_account.config(text=f"Current Account: {accounts[current_account_index]['username']}")
            else:
                label_current_account.config(text=f"All actions completed for all accounts")
            messagebox.showinfo(action_label, f"{action_label} completed for {username}")
            # Ask the user to select the next action for the new account
            action_var.set(None)

    threading.Thread(target=wrapper).start()

def view_story():
    user = entry_story_user.get()
    def action():
        try:
            id_usr = cl.user_id_from_username(user)
            time.sleep(5)
            lst_stories = cl.user_stories(id_usr)
            usr_str_pks = [lstus.pk for lstus in lst_stories]
            time.sleep(3)
            cl.story_seen(usr_str_pks)
        except Exception as e:
            messagebox.showerror("Story View", f"Failed to view {user}'s story: {e}")

    perform_action(action, "Story View")

def send_message():
    message = entry_message.get()
    usernames = entry_usernames.get().split(',')
    if not message:
        messagebox.showerror("Error", "Please enter a message to send.")
        return
    if not usernames:
        messagebox.showerror("Error", "Please enter usernames to send the message to.")
        return

    def action():
        lst_usernames=[]
        try:
            for username in usernames:
                username = username.strip()
                if username:
                    user_id = cl.user_id_from_username(username)
                    time.sleep(3)
                    lst_usernames.append(user_id)
            cl.direct_send(message,user_ids=lst_usernames)        
        except Exception as e:
            messagebox.showerror("Send Message", f"Failed to send message to {username}: {e}")

    perform_action(action, "Send Message")

def like_story():
    user = entry_story_user.get()
    
    def action():
        try:
            id_usr = cl.user_id_from_username(user)
            time.sleep(5)
            lst_stories = cl.user_stories(id_usr)
            for story in lst_stories:
                cl.story_like(story.pk)
        except Exception as e:
            messagebox.showerror("Like Story", f"Failed to like {user}'s story: {e}")

    perform_action(action, "Like Story")

def follow():
    user = entry_follow_user.get()
    def action():
        try:
            cl.user_follow(cl.user_id_from_username(user))
        except Exception as e:
            messagebox.showerror("Follow", f"Failed to follow {user}: {e}")

    perform_action(action, "Follow")

def unfollow():
    user = entry_follow_user.get()
    def action():
        try:
            cl.user_unfollow(cl.user_id_from_username(user))
        except Exception as e:
            messagebox.showerror("Unfollow", f"Failed to unfollow {user}: {e}")

    perform_action(action, "Unfollow")

def comment():
    post_url = entry_post_url.get()
    comment_text = entry_comment.get()
    def action():
        try:
            media_id = cl.media_id(cl.media_pk_from_url(post_url))
            time.sleep(2)  # Delay to prevent spam
            cl.media_comment(media_id, comment_text)
        except Exception as e:
            messagebox.showerror("Comment", f"Failed to post comment: {e}")

    perform_action(action, "Comment")

def scrape_followers():
    usernames = entry_usernames.get().split(',')
    if not usernames:
        messagebox.showerror("Error", "Please enter usernames to scrape followers.")
        return

    def action():
        all_followers_data = {}
        for username in usernames:
            username = username.strip()
            if username:
                try:
                    user_id = cl.user_id_from_username(username)
                    user_info=cl.user_info(user_id)
                    time.sleep(7)
                    followers = cl.user_followers(user_id)
                    time.sleep(6)
                    followers_data = []
                    for follower in followers.values():
                        followers_data.append(follower.username)
                    
                    all_followers_data[username] = {"followers":followers_data, "email":user_info.public_email,"phone":user_info.contact_phone_number}
                except Exception as e:
                    messagebox.showerror("Scrape Followers", f"Failed to scrape followers for {username}: {e}")
        with open('followers_data.json', 'w') as file:
            json.dump(all_followers_data, file, indent=4)

    perform_action(action, "Scrape Followers")

def on_closing():
    try:
        cl.logout()
    except Exception as e:
        print(f"Error during logout: {e}")
    root.destroy()

def show_processing_overlay():
    processing_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
    processing_label.config(text="Processing...")

def hide_processing_overlay():
    processing_label.config(text="")
    processing_overlay.place_forget()

def show_message_inputs():
    entry_post_url.grid_forget()
    entry_comment.grid_forget()
    entry_story_user.grid_forget()
    entry_follow_user.grid_forget()
    entry_message.grid(row=8, column=1, padx=10, pady=5)
    entry_usernames.grid(row=9, column=1, padx=10, pady=5)

def show_like_story_inputs():
    entry_post_url.grid_forget()
    entry_comment.grid_forget()
    entry_story_user.grid(row=6, column=1, padx=10, pady=5)
    entry_follow_user.grid_forget()
    entry_message.grid_forget()
    entry_usernames.grid_forget()

def show_follow_inputs():
    entry_post_url.grid_forget()
    entry_comment.grid_forget()
    entry_story_user.grid_forget()
    entry_follow_user.grid(row=7, column=1, padx=10, pady=5)
    entry_message.grid_forget()
    entry_usernames.grid_forget()

def show_unfollow_inputs():
    entry_post_url.grid_forget()
    entry_comment.grid_forget()
    entry_story_user.grid_forget()
    entry_follow_user.grid(row=7, column=1, padx=10, pady=5)
    entry_message.grid_forget()
    entry_usernames.grid_forget()

def show_comment_inputs():
    entry_post_url.grid(row=4, column=1, padx=10, pady=5)
    entry_comment.grid(row=5, column=1, padx=10, pady=5)
    entry_story_user.grid_forget()
    entry_follow_user.grid_forget()
    entry_message.grid_forget()
    entry_usernames.grid_forget()

def show_view_story_inputs():
    entry_post_url.grid_forget()
    entry_comment.grid_forget()
    entry_story_user.grid(row=6, column=1, padx=10, pady=5)
    entry_follow_user.grid_forget()
    entry_message.grid_forget()
    entry_usernames.grid_forget()

def show_scrape_followers_inputs():
    entry_post_url.grid_forget()
    entry_comment.grid_forget()
    entry_story_user.grid_forget()
    entry_follow_user.grid_forget()
    entry_message.grid_forget()
    entry_usernames.grid(row=9, column=1, padx=10, pady=5)

# GUI setup
root = tk.Tk()
root.title("Instagram Bot")
root.geometry("1400x600")  # Increased window size

tk.Label(root, text="Action", font=('Arial', 14)).grid(row=0, column=0, padx=10, pady=5)

action_var = tk.StringVar()
action_var.set(None)

tk.Radiobutton(root, text="Send Message", variable=action_var, value="Send Message", font=('Arial', 12),
               command=show_message_inputs).grid(row=1, column=0, padx=10, pady=5)
tk.Radiobutton(root, text="Like Story", variable=action_var, value="Like Story", font=('Arial', 12),
               command=show_like_story_inputs).grid(row=1, column=1, padx=10, pady=5)
tk.Radiobutton(root, text="Follow", variable=action_var, value="Follow", font=('Arial', 12),
               command=show_follow_inputs).grid(row=1, column=2, padx=10, pady=5)
tk.Radiobutton(root, text="Unfollow", variable=action_var, value="Unfollow", font=('Arial', 12),
               command=show_unfollow_inputs).grid(row=1, column=3, padx=10, pady=5)
tk.Radiobutton(root, text="Comment", variable=action_var, value="Comment", font=('Arial', 12),
               command=show_comment_inputs).grid(row=1, column=4, padx=10, pady=5)
tk.Radiobutton(root, text="View Story", variable=action_var, value="View Story", font=('Arial', 12),
               command=show_view_story_inputs).grid(row=1, column=5, padx=10, pady=5)
tk.Radiobutton(root, text="Scrape Followers", variable=action_var, value="Scrape Followers", font=('Arial', 12),
               command=show_scrape_followers_inputs).grid(row=1, column=6, padx=10, pady=5)

tk.Label(root, text="Message", font=('Arial', 14)).grid(row=8, column=0, padx=10, pady=5)
tk.Label(root, text="Story User", font=('Arial', 14)).grid(row=6, column=0, padx=10, pady=5)
tk.Label(root, text="User", font=('Arial', 14)).grid(row=7, column=0, padx=10, pady=5)
tk.Label(root, text="Post URL", font=('Arial', 14)).grid(row=4, column=0, padx=10, pady=5)
tk.Label(root, text="Comment", font=('Arial', 14)).grid(row=5, column=0, padx=10, pady=5)
tk.Label(root, text="Usernames (comma-separated)", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)

entry_message = tk.Entry(root, font=('Arial', 14), width=30)
entry_story_user = tk.Entry(root, font=('Arial', 14), width=30)
entry_follow_user = tk.Entry(root, font=('Arial', 14), width=30)
entry_post_url = tk.Entry(root, font=('Arial', 14), width=30)
entry_comment = tk.Entry(root, font=('Arial', 14), width=30)
entry_usernames = tk.Entry(root, font=('Arial', 14), width=30)


entry_message.grid(row=8, column=1, padx=10, pady=5)
entry_usernames.grid(row=9, column=1, padx=10, pady=5)
entry_story_user.grid_forget()
entry_follow_user.grid_forget()
entry_post_url.grid_forget()
entry_comment.grid_forget()

label_current_account = tk.Label(root, text=f"Current Account: {accounts[0]['username']}", font=('Arial', 14))
label_current_account.grid(row=10, column=0, columnspan=2, padx=10, pady=5)

tk.Button(root, text='Perform Action', command=lambda: action_var.get() == "Send Message" and send_message() or
                                                    action_var.get() == "Like Story" and like_story() or
                                                    action_var.get() == "Follow" and follow() or
                                                    action_var.get() == "Unfollow" and unfollow() or
                                                    action_var.get() == "Comment" and comment() or
                                                    action_var.get() == "View Story" and view_story() or
                                                    action_var.get() == "Scrape Followers" and scrape_followers(), 
          font=('Arial', 14), width=15).grid(row=11, column=1, pady=10)

# Processing overlay
processing_overlay = tk.Frame(root, bg='gray')
processing_label = tk.Label(processing_overlay, text="", font=('Arial', 20), bg='gray', fg='white')
processing_label.pack(expand=True)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
