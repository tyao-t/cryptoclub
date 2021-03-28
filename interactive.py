from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from cvs import *
from hourly_checknalert import getPriceMsg
app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    message_received = request.form['Body']
    message_to_send = "";
    mra = message_received.split(' ');
    print(mra);
    currency_name = mra[0];

    news_response = getNews(currency_name, num=1)
    news0 = news_response["articles"][0];
    news0_message_to_convey = "1. " + news0["title"] + ".\n" + \
    "per " + news0["source"]["name"] + ": " + news0["url"] + "\n"

    reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"),
                         client_secret=os.getenv("REDDIT_CLIENT_SECRET"), password=os.getenv("REDDIT_PASSWORD"),
                         user_agent='PRAW', username=os.getenv("REDDIT_USER_NAME"))

    #print(reddit.user.me())
    reddit_message_to_convey = f"Hot discussion on {currency_name} since last hour:\n"

    for post in reddit.subreddit(currency_name).top("day", limit=1):
        reddit_message_to_convey += f"{post.title} {post.url} {post.ups} upvotes, {post.num_comments} comments.\n"

    ai_advice_message_to_convey = "AI Advice: " + getAIAdvice(currency_name)["conclusion"] \
    + ".\n"

    if (len(mra) == 1):
        message_to_send += f"{currency_name}'s current price is {getCurrentPrice(currency_name)[0:7]} USD.\n\n"
        message_to_send += f"News headlines on {currency_name}:\n{news0_message_to_convey}\n"
        message_to_send += reddit_message_to_convey + "\n"
        message_to_send += ai_advice_message_to_convey
        message_to_send += "\n"
    else:
        for attr in mra:
            if (attr == "price"):
                message_to_send += getPriceMsg(currency_name)
                message_to_send += "\n"
            elif (attr == "news"):
                message_to_send += f"News headlines on {currency_name}:\n{news0_message_to_convey}"
                message_to_send += "\n"
            elif (attr == "discussion"):
                message_to_send += reddit_message_to_convey
                message_to_send += "\n"
            elif (attr == "advice"):
                message_to_send += ai_advice_message_to_convey
                message_to_send += "\n"
            else:
                pass

    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()

    # Add a message
    resp.message(message_to_send)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
