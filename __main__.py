import fb_posts
import read_emails

fb_posts.set_access_token(input())
read_emails.set_access_token(input())

fb_posts.fetch_and_post()
