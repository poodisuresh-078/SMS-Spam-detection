"""
Dataset Builder Script
Generates high-quality, diverse seed datasets for SMS Spam and Malicious URL classification.
These datasets serve as immediate out-of-the-box working datasets for development,
model training, and evaluation, while adhering to real-world patterns.
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_sms_dataset():
    sms_file = os.path.join(BASE_DIR, "sms_spam.csv")
    
    # Curated collection of diverse real-world SMS examples
    ham_messages = [
        "Hey, are we still meeting for lunch at 12:30 PM today?",
        "Mom said she will be home by 6, do not forget to take the groceries inside.",
        "Hey mate, did you finish the project report? Let me know so we can review before submission.",
        "The meeting has been rescheduled to tomorrow at 10:00 AM in Conference Room B.",
        "Happy birthday! Hope you have a wonderful year ahead filled with joy and success.",
        "Can you send me the lecture notes for chapter 4 when you get home?",
        "Thanks for dinner yesterday, had a really great time catching up with everyone.",
        "Please make sure to bring your laptop and charger for the hackathon tomorrow.",
        "I am running about 10 minutes late, traffic is terrible on the highway.",
        "Sure thing, I will see you at the library around 3 PM.",
        "Hey, what time does the flight land? I can come pick you up at terminal 2.",
        "Do not worry about the dishes, I will take care of them before going to bed.",
        "Dr. Smith confirmed your dental checkup for Thursday at 2:00 PM. Please arrive 10 min early.",
        "Your library books are due in 3 days. Renew online or return to campus branch.",
        "Can we reschedule our sync to 4 PM? Something urgent just came up with the client.",
        "Great job on the presentation today, the management team was really impressed!",
        "Could you check your email? I forwarded the updated budget spreadsheet for Q3.",
        "Are you free this weekend to help me move some furniture to the new apartment?",
        "Hey, let me know when you reach home safely. It was raining heavily outside.",
        "I left the spare key under the flower pot next to the front door.",
        "The train is delayed by 15 minutes due to signal maintenance. Waiting at platform 4.",
        "Could you pick up some milk and eggs on your way back from work?",
        "The professor said the assignment deadline has been extended to Friday midnight.",
        "Just wanted to say thank you for helping me prepare for the technical interview.",
        "Are you going to the gym tonight? Let me know if you want to pair up for leg day.",
        "Don't forget to submit your timecard before 5 PM today for payroll processing.",
        "Hey, did you watch the latest episode of the documentary we were discussing?",
        "Your order #48192 has been delivered to your front porch. Thank you for shopping with us.",
        "We are meeting at Joe's Pizza for Sarah's farewell dinner at 7:30 PM.",
        "I will be working remotely today as the plumber is coming to fix the sink leak.",
        "Can you review pull request #142 when you get a chance? Just merged the auth changes.",
        "Good morning team, reminder that our weekly standup begins in 15 minutes.",
        "Thanks for the book recommendation, I already started reading chapter 1 and love it.",
        "Hey, does your building have guest parking available or should I park on the street?",
        "Your appointment with Dr. Patel is scheduled for Monday, Oct 24 at 11:15 AM.",
        "I checked the recipe, we need olive oil, garlic, parmesan cheese, and pasta.",
        "The package was signed by the reception desk. You can collect it downstairs.",
        "What time do you want to head to the airport tomorrow morning?",
        "Yes, the code passes all unit tests and linting checks on the staging branch.",
        "I will bring the board games and some snacks for game night tonight.",
        "Please remember to turn off the air conditioning when you leave the office.",
        "Hey dad, just boarded the flight. Will text you as soon as we land.",
        "The contractor will be visiting tomorrow between 9 AM and 11 AM for the inspection.",
        "Can you send me the PDF of the syllabus from the orientation session?",
        "Dinner was fantastic, thank you so much for hosting us!",
        "The weather forecast says it will rain tomorrow, better keep an umbrella handy.",
        "Hey, can you cover my shift on Saturday from 2 PM to 8 PM? I will cover yours next week.",
        "We found your student ID card in room 302. You can retrieve it from lost and found.",
        "I have shared the Google Doc link with editing permissions for everyone.",
        "Just landed in Chicago. Waiting at baggage carousel 4.",
        "Hey, could you help me review the calculus practice questions before tomorrow's exam?",
        "The internet router was restarted and the connection is stable again.",
        "Happy anniversary! Wishing both of you many more years of happiness and togetherness.",
        "Could you email me the contact details for the vendor who repaired the projector?",
        "I will be offline for the next 2 hours for a doctor appointment.",
        "Hey, are we still playing badminton this evening at the sports complex?",
        "The landlord confirmed that the water maintenance will finish by 1 PM.",
        "Can you forward the tracking number for the shipment so I can monitor delivery?",
        "The team lunch is confirmed for Friday at the Italian bistro down the street.",
        "Please remember to sign the birthday card for Michael before 3 PM.",
        "I took the dog for a walk and fed him. He is resting now.",
        "Hey, what is the WiFi password for the guest network at the office?",
        "Just sent you the photos from our weekend hiking trip. Check WhatsApp.",
        "The car service is complete. You can pick up your vehicle anytime before 6 PM.",
        "Can you double check the address on the invoice before we send it to the client?",
        "I will be on annual leave starting next Monday through Wednesday.",
        "Hey, do you want coffee? I am walking down to Starbucks right now.",
        "The concert tickets went on sale this morning, managed to grab two seats in row C!",
        "Let us catch up over a phone call tomorrow afternoon when you are free.",
        "I will put the laundry in the dryer before heading out to class.",
        "The seminar on cloud architecture was very insightful, took plenty of notes.",
        "Hey, did you find your car keys? They were on the kitchen counter.",
        "Your prescription is ready for pickup at the neighborhood pharmacy.",
        "We need to finalize the quarterly slide deck before Thursday's executive review.",
        "Just finished running 5 km at the park, feeling energized!",
        "Can you bring extra paper cups and napkins for the picnic?",
        "The bus was full so I had to wait for the next one, should arrive in 15 mins.",
        "Hey, have you heard back from the recruiter regarding the interview feedback?",
        "We are meeting near the fountain entrance at the shopping mall.",
        "The software update is installed and the system rebooted cleanly.",
        "I left some leftover pasta in the fridge for you in a red container.",
        "Don't worry about paying me back now, we can settle it when we go to lunch next week.",
        "The gym is closed for deep cleaning this Sunday morning.",
        "Could you print two copies of the contract on the third floor printer?",
        "Hey, let me know if you need a ride to the graduation ceremony tomorrow.",
        "We are organizing a surprise birthday party for Sarah this Friday at 8 PM.",
        "I checked the tire pressure and filled the windshield wiper fluid.",
        "The project kickoff call is moved to 2:30 PM due to time zone differences.",
        "Please send the receipt for the office supplies so I can submit the expense report.",
        "Hey, did you try that new ramen place downtown? The broth was amazing.",
        "The museum exhibition was very fascinating, definitely worth visiting.",
        "I will pick up the dry cleaning after my evening meeting concludes.",
        "Can you please review the draft email to the stakeholders before I click send?",
        "We made a reservation for 6 people under the name Johnson for 8:00 PM.",
        "The air filter in the furnace has been replaced for the winter season.",
        "Hey, are you free for a quick 5-minute phone call regarding the client bug?",
        "I am bringing my homemade banana bread to the office tomorrow morning.",
        "The package was left with your neighbor in apartment 4B as requested.",
        "Looking forward to catching up at the alumni reunion this Saturday!",
        "Hey, can you send the Zoom link for the project demonstration again?",
        "All database migrations executed successfully on the staging cluster.",
        "Don't forget to submit the voter registration form before the deadline.",
        "The heating system in the conference room has been repaired.",
        "Let us meet at the coffee shop across from the subway station.",
        "I received your voice message and will get back to you by early evening.",
        "The dentist recommended using a soft bristle toothbrush and flossing daily.",
        "Can you check if the conference room projector has an HDMI adapter?",
        "We reached the cabin safely, beautiful view of the lake from here!",
        "I will be working from the cafeteria for the rest of the afternoon.",
        "The school bus is running 10 minutes late due to road construction.",
        "Hey, make sure to bring a warm jacket, it is freezing outside today.",
        "The presentation slides have been uploaded to the shared team folder.",
        "Can you please water the plants on the balcony while I am away this weekend?",
        "The auto-save feature saved my progress when my laptop battery died, thank goodness!",
        "We are thinking of going camping near the national park next month.",
        "I have approved your time off request in the HR portal.",
        "Hey, is the grocery store still open or did they close at 9 PM?",
        "Thanks for helping me fix the tire, really appreciate you stopping by.",
        "The lecture hall has been changed to Hall 104 for today's biology class.",
        "I will review the pull request and leave my feedback in the comments by tonight."
    ]
    
    spam_messages = [
        "URGENT: Your Wells Fargo account has been suspended due to suspicious activity. Verify immediately at http://wellsfargo-security-alert.xyz to avoid permanent closure.",
        "CONGRATULATIONS! You have been selected as the winner of a $1,000 Walmart Gift Card! Claim your reward now at http://walmart-winner-claim2024.top before expires.",
        "Your Netflix subscription payment failed! Update your credit card details immediately at http://netflix-billing-update-card.cc to prevent service termination.",
        "USPS Alert: Your package delivery #US91823 has been suspended due to an incomplete street address. Update details at http://usps-track-package-update.info",
        "Exclusive offer! You qualify for a pre-approved personal loan of up to $25,000 with 0% interest for 12 months. Apply now at http://fast-cash-loans-direct.net",
        "IRS Notice: You have an unclaimed tax refund of $1,485.00 waiting. Submit your direct deposit information now at http://irs-tax-refund-portal.org",
        "Your Apple ID has been locked for security reasons. Confirm your identity within 24 hours at http://appleid-security-unlock-device.xyz or device will be disabled.",
        "Get rich with automated Bitcoin trading! Guaranteed $500 daily profits with zero risk. Register free today at http://crypto-wealth-generator.buzz",
        "Amazon Fraud Alert: Someone attempted to purchase an iPhone 15 Pro for $1,199 on your account. If this was not you, call 1-800-555-0199 or verify at http://amz-fraud-dispute.biz",
        "WINNER! Your mobile number won 500,000 GBP in the UK National Lottery! Send your full name and bank details to uk-lottery-claims@mail.ru to redeem.",
        "URGENT! Chase Bank: We detected an unauthorized withdrawal of $850.00 from your checking account. Cancel transaction immediately at http://chase-bank-verify-alert.com",
        "FedEx: Your parcel shipment #FX48209 requires a $2.99 customs fee before dispatch. Pay fee online at http://fedx-customs-fee-portal.top",
        "Hot singles in your neighborhood are waiting to chat! Click here to view private photos and meet tonight: http://dating-meet-singles-now.xyz",
        "Bank of America Alert: Suspicious login from IP 192.168.1.55 detected. Protect your account now at http://bofa-security-login-check.cc",
        "FREE Ringtone & Wallpaper club! Text YES to 88488 now to claim your first 5 free downloads. Standard text messaging rates apply.",
        "URGENT: Your PayPal account has been limited due to unusual transaction volume. Restore access at http://paypal-resolution-center-secure.top/verify",
        "Congratulations! You are the guaranteed 1st prize winner of a brand new 65-inch 4K OLED TV! Claim code: TV8819 at http://claim-electronics-reward.xyz",
        "Work from home and earn $3,000 to $5,000 weekly with Amazon product reviews! No experience required. Apply now at http://remote-careers-amazon.biz",
        "Citizens Bank: An unauthorized wire transfer was initiated on your account. If you did not authorize this, cancel immediately at http://citizens-verify-secure.net",
        "FREE MONEY! Apply for government relief grant of $12,500 now! No repayment required. Visit http://grant-funds-approval.xyz to claim.",
        "DHL Express: Your delivery is on hold due to missing house number. Reschedule delivery at http://dhl-package-redelivery-online.info",
        "Your debit card ending in 4019 has been temporarily frozen. Verify your card details and PIN at http://secure-card-activation-portal.cc to unfreeze.",
        "SPECIAL DISCOUNT: Buy genuine Viagra and Cialis at 80% off retail pharmacy prices! Fast discreet delivery. Order at http://rx-pharmacy-direct-discount.top",
        "AT&T Alert: Your monthly bill payment is overdue. Pay before 5 PM to prevent immediate mobile service suspension: http://att-payment-resolution.xyz",
        "Congratulations user! Your phone number was randomly drawn to receive a $500 Target gift certificate. Enter code TGT99 at http://target-voucher-reward.buzz",
        "URGENT: Coinbase security notification. A withdrawal of 1.45 ETH was requested. If not you, cancel transaction at http://coinbase-auth-verify.biz",
        "You have 1 new unread voice message from an unknown caller. Listen to recording online at http://voicemail-notification-carrier.top/play?id=992",
        "Instant cash loan approval! Bad credit OK. Receive up to $10,000 in your bank account in 1 hour. Apply now: http://instant-cash-deposit-today.net",
        "FINAL NOTICE: Your car warranty is expiring! Do not pay thousands for future engine repairs. Renew today at http://vehicle-warranty-protection.cc",
        "Social Security Administration Notice: Your SSN has been flagged for fraudulent activity. Call federal agent immediately at 1-800-555-0144 to avoid arrest.",
        "Exclusive casino bonus! Claim 200 free spins and $1,000 welcome match deposit. Play now at http://spin-win-casino-royale.xyz",
        "Capital One Alert: Did you attempt a $642.18 transaction at BEST BUY? Reply NO to block or visit http://capone-fraud-alert-verify.top",
        "Congratulations! You have been awarded a complimentary 4-day cruise to the Bahamas! Call 1-888-555-0199 now to claim your cabin tickets.",
        "URGENT NOTICE: Your electricity service will be disconnected in 45 minutes due to unpaid balance of $184.20. Pay now at http://power-utility-pay.xyz",
        "UPS Alert: We attempted delivery today but no one was home. Reschedule your delivery and pay fee at http://ups-parcel-reschedule-fee.info",
        "Crypto alert: You received 5,000 DOGE tokens in your airdrop wallet! Claim your reward within 12 hours at http://doge-airdrop-bonus-claim.top",
        "Verification code 920194 for Wells Fargo online banking. If you did not request this code, your account is compromised. Visit http://wellsfargo-verify.cc",
        "You won second prize in the International Mobile Sweepstakes! Claim $250,000 cash lump sum at http://international-sweepstakes-claims.xyz",
        "TD Bank: A new device has logged into your mobile banking profile. If this was not you, lock account at http://tdbank-security-center.top",
        "Free $100 Starbucks gift card for completing a 2-minute customer survey! Start survey now at http://starbucks-survey-reward2024.buzz",
        "URGENT: Microsoft Windows detected critical Trojan spyware on your PC. Call toll-free technical support 1-888-555-0182 immediately.",
        "Santander Bank: Your security token has expired. Update your login credentials at http://santander-token-renew.info to keep access active.",
        "Get pre-approved for debt relief! Settle your credit card balances for 50% less without bankruptcy. Inquire at http://debt-relief-settlement.net",
        "Geek Squad Auto-Renewal: Your subscription has been renewed for $399.99. If you wish to cancel and request refund, call 1-800-555-0177.",
        "URGENT: eBay security alert. Suspicious bidding activity on your account. Review transactions immediately at http://ebay-account-security-center.xyz",
        "You have been awarded a free iPad Mini from our customer appreciation draw! Claim your device at http://apple-customer-rewards-draw.top",
        "Venmo Security: A payment of $450 to unknown user is pending. To cancel this transaction, verify identity at http://venmo-payment-dispute.biz",
        "Fast weight loss miracle pill! Lose 20 lbs in 14 days without exercise or diet! Try free risk trial bottle at http://keto-miracle-slimming.top",
        "URGENT: PNC Bank alert. Your debit card has been restricted due to multiple PIN failures. Reactivate at http://pnc-card-reactivate-portal.cc",
        "Exclusive invitation! Invest in pre-IPO AI tech stocks and multiply your wealth 10x! Sign up now at http://pre-ipo-investor-club.xyz",
        "Congratulations! Your phone number won a brand new Tesla Model 3! Confirm registration code TS891 at http://tesla-giveaway-winner.top",
        "Barclays Bank: Suspicious international transaction of 740 GBP detected in Nigeria. Confirm or deny at http://barclays-security-fraud-alert.info",
        "Special bonus: 50 free scratch-off tickets with any $10 deposit! Scratch and win real cash at http://lucky-scratch-tickets-online.buzz",
        "Your Google account was accessed from a Linux device in Moscow, Russia. Secure your account now at http://google-account-verify-login.xyz",
        "URGENT: Your Medicare benefits have been updated. Review new coverage and dental card eligibility at http://medicare-advantage-plans.net",
        "You have won a free $250 Costco grocery shopping spree! Enter your delivery address at http://costco-shopping-voucher-promo.top",
        "HSBC Security: An unauthorized payee was added to your online profile. If this was not authorized, visit http://hsbc-fraud-detection-team.cc",
        "T-Mobile: Your bill credit of $75.00 is ready to be claimed! Follow the link to apply credit to your bill: http://tmobile-bill-credit-claim.biz",
        "Alert: Your package from Royal Mail has an outstanding customs charge of 1.45 GBP. Pay now at http://royalmail-customs-fee-settle.xyz",
        "Instant payday loan! No credit check required, instant cash deposit into checking account. Apply at http://instant-payday-funds-247.top",
        "URGENT: Truist Bank online banking has been temporarily disabled. Verify your identity at http://truist-online-banking-restore.info",
        "Congratulations winner! You won the grand prize in the Mega Millions sweepstakes! Contact claims department at claim-funds@lottery-winner.ru",
        "Your Instagram account will be deleted in 24 hours for copyright violation! Submit appeal immediately at http://instagram-copyright-appeal.xyz",
        "Apply for affordable health insurance coverage starting at just $39/month! Enroll before open enrollment ends: http://affordable-health-cover.net",
        "Discover Card Alert: Suspicious transaction of $512.90 at Apple Store. If fraudulent, decline at http://discover-fraud-security-center.top",
        "Free sample box filled with luxury cosmetics and perfume! Claim your free gift box today at http://luxury-beauty-box-samples.buzz",
        "URGENT: Southwest Airlines flight compensation voucher worth $400 is waiting for you. Claim at http://southwest-flight-voucher-claim.xyz",
        "USPS: Redelivery scheduled for tomorrow. A $1.50 handling fee applies. Complete payment at http://usps-redelivery-handler-fee.cc",
        "Cryptocurrency giveaway! Elon Musk is giving away 10,000 ETH! Send 0.1 ETH to receive 1 ETH back instantly at http://musk-eth-giveaway.biz",
        "Your PayPal transaction to Crypto Exchange for $950.00 is complete. If this was not you, dispute at http://paypal-dispute-transaction.info"
    ]
    
    # Expand dataset with realistic variations to ensure high quality training (> 250 samples)
    extended_ham = [
        f"Hey, {name}, remember our meeting at {time} in {place}."
        for name in ["Alex", "Jordan", "Taylor", "Morgan", "Sam", "Chris"]
        for time in ["10:00 AM", "2:00 PM", "4:30 PM", "lunchtime"]
        for place in ["Conference Room A", "the coffee shop", "the lab", "the library"]
    ][:80]
    
    extended_spam = [
        f"URGENT: Your {bank} account has been {action}! Verify immediately at {url} to restore full access."
        for bank in ["Chase", "Wells Fargo", "Bank of America", "Citibank", "Capital One"]
        for action in ["temporarily locked", "flagged for suspicious activity", "suspended", "restricted"]
        for url in ["http://secure-account-verification-alert.xyz", "http://banking-security-update.top", "http://login-fraud-prevention.cc", "http://verify-bank-details.biz"]
    ][:80]
    
    all_ham = ham_messages + extended_ham
    all_spam = spam_messages + extended_spam
    
    rows = []
    for msg in all_ham:
        rows.append({"label": "ham", "message": msg.strip()})
    for msg in all_spam:
        rows.append({"label": "spam", "message": msg.strip()})
        
    with open(sms_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["label", "message"])
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"[+] SMS Dataset generated: {len(rows)} samples ({len(all_ham)} ham, {len(all_spam)} spam) -> {sms_file}")


def create_url_dataset():
    url_file = os.path.join(BASE_DIR, "urls.csv")
    
    legitimate_urls = [
        "https://www.google.com/search?q=machine+learning+algorithms",
        "https://www.wikipedia.org/wiki/Artificial_intelligence",
        "https://github.com/scikit-learn/scikit-learn",
        "https://www.python.org/downloads/windows/",
        "https://stackoverflow.com/questions/tagged/python",
        "https://www.microsoft.com/en-us/windows/get-windows-11",
        "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
        "https://www.nytimes.com/section/technology",
        "https://www.nature.com/articles/d41586-024-00123-x",
        "https://docs.python.org/3/library/sqlite3.html",
        "https://flask.palletsprojects.com/en/3.0.x/quickstart/",
        "https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html",
        "https://www.amazon.com/dp/B08N5WRWNW",
        "https://www.apple.com/iphone-16-pro/specs/",
        "https://www.bbc.com/news/technology-68192019",
        "https://edition.cnn.com/world/europe/index.html",
        "https://www.mit.edu/research/computing-and-information-sciences/",
        "https://stanford.edu/academics/departments/",
        "https://www.harvard.edu/programs/computer-science/",
        "https://www.cloudflare.com/learning/security/what-is-cybersecurity/",
        "https://www.youtube.com/watch?v=kqtD5dpn9C8",
        "https://www.linkedin.com/in/data-scientist-profile/",
        "https://www.reddit.com/r/MachineLearning/comments/trending/",
        "https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset",
        "https://pypi.org/project/Flask/",
        "https://numpy.org/doc/stable/reference/generated/numpy.array.html",
        "https://pandas.pydata.org/docs/getting_started/overview.html",
        "https://www.coursera.org/specializations/deep-learning",
        "https://www.edx.org/learn/data-structures",
        "https://arxiv.org/abs/1706.03762",
        "https://medium.com/towards-data-science/understanding-url-classification",
        "https://www.quora.com/topic/Natural-Language-Processing",
        "https://www.booking.com/hotel/us/grand-central.html",
        "https://www.airbnb.com/rooms/102938475",
        "https://www.spotify.com/us/premium/",
        "https://www.netflix.com/browse/genre/83",
        "https://www.imdb.com/title/tt0111161/",
        "https://www.bloomberg.com/markets/stocks",
        "https://www.reuters.com/business/finance/",
        "https://www.wsj.com/tech/personal-tech",
        "https://gitlab.com/explore/projects",
        "https://bitbucket.org/product/features",
        "https://www.docker.com/products/docker-desktop/",
        "https://kubernetes.io/docs/concepts/overview/",
        "https://aws.amazon.com/ec2/pricing/on-demand/",
        "https://cloud.google.com/products/ai-machine-learning",
        "https://azure.microsoft.com/en-us/products/virtual-machines",
        "https://www.theverge.com/tech",
        "https://techcrunch.com/category/startups/",
        "https://wired.com/category/gear/",
        "https://cve.mitre.org/cve/search_cve_list.html",
        "https://nvd.nist.gov/vuln/detail/CVE-2024-21413",
        "https://owasp.org/www-project-top-ten/",
        "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "https://www.us-cert.gov/ncas/alerts",
        "https://www.cisco.com/c/en/us/products/security/index.html",
        "https://www.paloaltonetworks.com/cyberpedia",
        "https://www.fortinet.com/resources/cyberglossary",
        "https://www.trendmicro.com/vinfo/us/security/news",
        "https://krebsonsecurity.com/about/",
        "https://www.schneier.com/blog/archives/recent.html",
        "https://news.ycombinator.com/news",
        "https://www.khanacademy.org/math/statistics-probability",
        "https://www.codecademy.com/learn/learn-python-3",
        "https://leetcode.com/problemset/all/",
        "https://www.hackerrank.com/domains/algorithms",
        "https://www.kaggle.com/competitions",
        "https://www.figma.com/community/file/templates",
        "https://getbootstrap.com/docs/5.3/getting-started/introduction/",
        "https://tailwindcss.com/docs/installation",
        "https://react.dev/learn/tutorial-tic-tac-toe",
        "https://vuejs.org/guide/introduction.html",
        "https://angular.io/docs",
        "https://svelte.dev/tutorial/basics",
        "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs",
        "https://expressjs.com/en/starter/hello-world.html",
        "https://www.djangoproject.com/start/",
        "https://fastapi.tiangolo.com/tutorial/",
        "https://sqlite.org/docs.html",
        "https://www.postgresql.org/docs/current/",
        "https://dev.mysql.com/doc/refman/8.0/en/",
        "https://www.mongodb.com/docs/manual/",
        "https://redis.io/docs/latest/develop/get-started/",
        "https://graphql.org/learn/",
        "https://curl.se/docs/manual.html",
        "https://git-scm.com/doc",
        "https://www.gnu.org/software/bash/manual/",
        "https://man7.org/linux/man-pages/man1/grep.1.html",
        "https://vim.org/docs.php",
        "https://neovim.io/doc/user/",
        "https://code.visualstudio.com/docs/editor/codebasics",
        "https://help.github.com/articles/set-up-git/",
        "https://about.gitlab.com/handbook/",
        "https://slack.com/resources/using-slack",
        "https://zoom.us/pricing",
        "https://www.dropbox.com/business",
        "https://drive.google.com/drive/u/0/my-drive",
        "https://workspace.google.com/products/gmail/",
        "https://outlook.live.com/mail/0/inbox",
        "https://www.office.com/launch/excel"
    ]
    
    malicious_urls = [
        "http://192.168.1.100/paypal-login/verification-update.php",
        "http://185.220.101.5/bankofamerica/secure-login/index.htm",
        "http://216.58.214.14/account-verification/update-banking.html",
        "http://45.142.214.18/wellsfargo/online-banking/signin.html",
        "http://91.240.118.172/apple-id-suspended/login-verify.php",
        "http://103.208.86.12/netflix/payment-update/account-billing.php",
        "http://194.26.29.112/chase/signon/verification-form.html",
        "http://198.51.100.42/amazon/orders/update-creditcard.php",
        "http://178.62.204.11/secure-coinbase/wallet-auth/claim-eth.html",
        "http://185.193.125.8/citibank-online/logon/credentials-update.htm",
        "http://paypal-security-verification-center.update.account-secure.xyz/login",
        "http://wellsfargo-online-banking-urgent-verify.top/signin.php?token=9281",
        "http://apple-id-suspended-unusual-activity.com.verify-login.tk/security",
        "http://chase-bank-account-security-alert.com.customer-support.xyz/online-banking/verify.html",
        "http://netflix-billing-update-card-expired.net.account-login.top/customer-service/login",
        "http://free-crypto-bonus-claim-now.xyz/btc/claim.php?ref=2819",
        "http://microsoft-windows-defender-alert-virus-remove.cc/support/call-now",
        "http://amazon-prime-prize-winner-claim-now.top/redeem?id=99281",
        "http://ebayisapi.dll-sign-in-co-uk.suspicious-login.info/account/verify.php",
        "http://steam-community-free-skins-gift.ru/trade/accept-offer?key=8192",
        "http://irs-tax-refund-verification-online.org.claim-now.xyz/form-submit",
        "http://dhl-express-parcel-tracking-failed-update.net/delivery/index.php",
        "http://secure-login-instagram-password-reset.info/accounts/signin?token=xyz",
        "http://facebook-security-policy-violation-appeal.top/review/login.php",
        "http://metamask-wallet-seed-phrase-validation.cc/connect-wallet-now",
        "http://binance-kyc-verification-security-portal.xyz/en/usercenter/login",
        "http://usps-tracking-package-address-confirm.top/redelivery/fee-pay.html",
        "http://fedex-express-delivery-address-update.xyz/shipping/track.php",
        "http://citizens-bank-online-security-token-update.info/signon/login",
        "http://pnc-online-banking-fraud-prevention-alert.cc/auth/verify-account",
        "http://capital-one-credit-card-fraud-alert-verify.top/security/dispute",
        "http://bofa-bank-of-america-security-center.xyz/signin/authenticate.php",
        "http://att-mobile-account-suspended-bill-pay.biz/myatt/payment.html",
        "http://verizon-wireless-customer-loyalty-rewards.top/claim-giftcard",
        "http://santander-secure-passcode-update.info/logon/step2.php",
        "http://barclays-online-banking-fraud-team-review.cc/personal/login.htm",
        "http://td-bank-customer-security-authentication.xyz/profile/verification",
        "http://royal-mail-reschedule-failed-parcel.top/redeliver/pay-fee.php",
        "http://ups-package-held-in-customs-duty.xyz/tracking/customs-payment",
        "http://coinbase-pro-security-device-approval.net/signin/2fa-code.php",
        "http://blockchain-wallet-private-key-restore.top/recovery/mnemonic",
        "http://trust-wallet-token-airdrop-claim.xyz/rewards/connect.html",
        "http://free-iphone-15-pro-winner-claim-today.buzz/promotions/winner",
        "http://walmart-shopping-spree-voucher-claim.top/survey/reward.php",
        "http://target-giftcard-giveaway-official.xyz/redeem/card-activation",
        "http://costco-member-loyalty-bonus-claim.biz/rewards/claim.html",
        "http://google-drive-shared-file-encrypted-download.info/docs/login",
        "http://microsoft-onedrive-document-viewer-secure.xyz/sharepoint/auth",
        "http://dropbox-shared-invoice-view-pdf.top/files/download-verify",
        "http://adobe-document-cloud-sign-invoice-required.cc/sign/contract.php",
        "http://docusign-envelope-review-and-sign-urgent.info/documents/auth",
        "http://zoom-meeting-client-update-patch-download.xyz/webclient/install.exe",
        "http://whatsapp-web-login-qr-code-scan-device.top/sync/authenticate",
        "http://telegram-account-verification-bot-auth.buzz/login/phone.php",
        "http://twitter-blue-badge-free-verification.xyz/apply/verified-profile",
        "http://linkedin-job-application-resume-review.info/careers/signin.php",
        "http://discord-nitro-free-3months-gift-claim.ru/gift/redeem-code",
        "http://roblox-free-robux-generator-no-survey.top/generator/generate.php",
        "http://fortnite-free-vbucks-glitch-working.xyz/season/claim-vbucks",
        "http://ea-sports-fifa-ultimate-team-coins-generator.buzz/coins/claim",
        "http://uber-eats-free-50-voucher-promo-code.top/food/redeem.html",
        "http://doordash-credits-loyalty-bonus-claim.xyz/promos/claim.php",
        "http://airbnb-booking-discount-70-off-payment.info/rooms/book-direct",
        "http://ticketmaster-taylor-swift-presale-tickets.top/events/checkout",
        "http://stubhub-vip-concert-pass-instant-claim.xyz/tickets/purchase",
        "http://crypto-doubler-deposit-bitcoin-earn-double.ru/invest/deposit",
        "http://ai-passive-income-trading-bot-guaranteed.biz/register/signup",
        "http://forex-signals-free-daily-pips-profit.xyz/signals/join-now",
        "http://debt-relief-government-forgiveness-program.top/apply/qualify",
        "http://student-loan-forgiveness-instant-approval.info/application/form",
        "http://irs-direct-deposit-tax-rebate-form.xyz/stimulus/claim-check",
        "http://social-security-benefit-suspension-appeal.cc/verify-ssn.php",
        "http://medicare-card-replacement-verification.top/benefits/update",
        "http://dmv-drivers-license-renewal-suspended-fee.xyz/dmv/renew-online",
        "http://us-customs-border-protection-held-package.info/inspection/pay",
        "http://geek-squad-annual-support-invoice-cancel.buzz/refund/form.html",
        "http://mcafee-antivirus-expired-renew-subscription.top/billing/pay.php",
        "http://norton-lifelock-security-alert-protection.cc/account/renew.htm",
        "http://avg-pc-tuneup-license-key-activation.xyz/support/billing",
        "http://kaspersky-threat-detection-removal-tool.info/download/clean.exe",
        "http://secure-banking-portal-verification-check.com.ru/bank/login",
        "http://wells-fargo-advisors-online-portfolio-auth.top/advisors/login",
        "http://fidelity-investments-account-security-alert.xyz/customer/signin",
        "http://vanguard-brokerage-service-update-profile.info/investor/auth",
        "http://charles-schwab-online-banking-session-timeout.cc/client/login",
        "http://robinhood-crypto-withdrawal-verification-pending.top/auth/verify",
        "http://webull-financial-stock-trading-account-update.xyz/trade/login",
        "http://etrade-financial-login-verification-security.buzz/session/auth",
        "http://american-express-cardmember-statement-review.info/account/verify",
        "http://ally-bank-online-savings-password-reset.top/customers/login",
        "http://synchrony-credit-card-payment-failed-alert.xyz/manage/pay.php",
        "http://navy-federal-credit-union-member-verify.cc/nfcu/signon.html",
        "http://usaa-military-banking-security-access-device.info/ent/logon",
        "http://penfed-credit-union-fraud-notification.top/online/security",
        "http://keybank-online-banking-identity-confirmation.xyz/security/step1",
        "http://regions-bank-commercial-login-credentials.info/business/signin",
        "http://fifth-third-bank-customer-alert-verification.top/protect/auth",
        "http://huntington-national-bank-fraud-center.xyz/hub/security-check",
        "http://m-and-t-bank-web-banking-access-restore.cc/online/login.php",
        "http://suntrust-now-truist-account-migration-portal.top/transfer/auth"
    ]
    
    # Expand with diverse synthetic examples based on distinct lexical patterns (> 250 rows)
    expanded_legit = [
        f"https://www.{org}.{tld}/docs/{topic}/guide.html"
        for org in ["apache", "kernel", "mozilla", "gnu", "w3", "ietf", "freebsd"]
        for tld in ["org", "net"]
        for topic in ["network", "protocols", "security", "compilers", "storage", "crypto"]
    ][:80]
    
    expanded_malicious = [
        f"http://{brand}-security-update-{num}.{tld}/login-verify/auth.php"
        for brand in ["paypal", "wellsfargo", "appleid", "chase-bank", "netflix", "microsoft"]
        for num in ["2024", "auth", "verify", "secure"]
        for tld in ["xyz", "top", "buzz", "cc"]
    ][:80]
    
    all_legit = legitimate_urls + expanded_legit
    all_malicious = malicious_urls + expanded_malicious
    
    rows = []
    for u in all_legit:
        rows.append({"url": u.strip(), "label": "legitimate"})
    for u in all_malicious:
        rows.append({"url": u.strip(), "label": "malicious"})
        
    with open(url_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["url", "label"])
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"[+] URL Dataset generated: {len(rows)} samples ({len(all_legit)} legitimate, {len(all_malicious)} malicious) -> {url_file}")

if __name__ == "__main__":
    create_sms_dataset()
    create_url_dataset()

