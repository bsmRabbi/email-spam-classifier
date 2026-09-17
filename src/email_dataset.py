# Curated collection of classic email spam (419 advance-fee fraud, phishing, DMCA copyright extortion,
# fake invoices, package delivery scams) and legitimate email messages (work correspondence, legal notices, scheduling).
# This bridges the domain gap between short SMS texts (spam.csv) and real-world emails.

EMAIL_SAMPLES = [
    # --- DMCA & Copyright Extortion Phishing (SPAM) ---
    {
        "label_text": "spam",
        "text": """Hello, I am a professional photographer and the legal owner of the copyrighted images used on your website without my explicit permission or license. This unauthorized use constitutes a direct violation of intellectual property laws. I have documented the infringing pages and compiled them into a formal legal complaint. To avoid immediate legal action and a formal lawsuit for statutory damages, I demand that you review the infringing material and remove it from your servers immediately. You can view the specific list of copyrighted assets and the legal notice in the cloud repository link below: [View Copyright Infringement Notice Document (PDF)] If the material is not removed within 48 hours, my attorney will proceed with filing a formal Digital Millennium Copyright Act (DMCA) takedown notice and pursuing financial damages. Sincerely, Alex Rivera, Rivera Photography Studios"""
    },
    {
        "label_text": "spam",
        "text": """Notice of Copyright Infringement: We represent various copyright owners whose digital illustrations have been published on your domain without license. Failure to remove the infringing content within 24 hours will result in statutory copyright infringement litigation under the DMCA. Download and review the complete evidence file here: [Download Infringement Evidence Archive.zip]"""
    },

    # --- 419 / Advance-Fee / African Dignitary / Fund Transfer Scams (SPAM) ---
    {
        "label_text": "spam",
        "text": """Hello, Greetings to you. Thanks for your quick response. A top VIP in one of the African Countries is in dire need of an entrepreneur or fund manager that can confidently receive and manage the sum of US$5.2 Billion with a reasonable return on investment annually. Please should you find this offer interesting, kindly revert back to me so we can discuss modalities that will perfect the transfer of the funds to any account you may deem safe. To make this happen, a meeting may be arranged where this transaction will be discussed one on one and measures will be streamlined for a successful completion of the transaction where applicable. Note: For your eligibility to handle this significant huge funds, you would have to own a company and operational bank account where the funds shall be transferred into for the investment purposes. Also, You must have a project plan to accommodate and invest the funds. Please feel free to contact me and i would be happy to provide further details. Regards, Mr. William Schneider"""
    },
    {
        "label_text": "spam",
        "text": """A top VIP in one of the African Countries is in dire need of an entrepreneur or fund manager that can confidently receive and manage the sum of US$5.2 Billion with a reasonable return on investment annually. Please should you find this offer interesting, kindly revert back to me so we can discuss modalities that will perfect the transfer of the funds to any account you may deem safe."""
    },
    {
        "label_text": "spam",
        "text": """Dearest Friend, I am Mrs. Mariam Sese-Seko, widow of late President Mobutu Sese-seko of Zaire. I have the sum of $25,000,000 USD deposited in a security company in Europe. I need a trustworthy foreign partner who will assist me in transferring these funds into their bank account for safe keeping and investment. You will be compensated with 25% of the total funds for your kind assistance. Reply urgently with your full name, telephone, and bank details."""
    },
    {
        "label_text": "spam",
        "text": """Urgent Assistance Required: I am Barrister David Morgan, personal attorney to a deceased foreign contractor who died in a tragic crash. He left behind an unclaimed sum of $18.5 Million in an offshore bank. As his legal counsel, the bank has notified me to present the next of kin or the funds will be confiscated. I seek your consent to present you to the bank as the bona fide beneficiary so the money can be wired into your bank account. We will share 50/50. Treat this with utmost confidentiality."""
    },
    {
        "label_text": "spam",
        "text": """ATTENTION: BENEFICIARY. We wish to inform you that your overdue payment of US$10.5 Million has been approved for immediate release by the United Nations Compensation Commission and Central Bank. Previous attempts failed due to corrupt officials. To receive your consignment box or wire transfer via Western Union, you must confirm your receiving bank details, copy of ID, and delivery address immediately to Mr. Kenneth Cole."""
    },

    # --- Fake Invoices / Renewal Scams (SPAM) ---
    {
        "label_text": "spam",
        "text": """INVOICE #9842 OVERDUE: Your subscription for Geek Squad BestBuy Protection has been renewed for $499.99 auto-debited from your checking account. If you did not authorize this charge, call our toll-free cancellation department immediately at +1-800-555-0199 for an instant refund within 24 hours."""
    },
    {
        "label_text": "spam",
        "text": """Dear Customer, Thank you for renewing your Norton 360 Security membership for $399.00 billed to your card. To dispute or cancel this charge, please contact our billing helpdesk at 1-888-234-9812."""
    },

    # --- Courier / Delivery Phishing (SPAM) ---
    {
        "label_text": "spam",
        "text": """USPS Notification: Your package delivery has been suspended due to an incomplete address. To reschedule your delivery and confirm your shipping information, click here: http://usps-tracking-redelivery-portal.com/update. A $1.50 redelivery fee applies."""
    },

    # --- Phishing & Account Takeover (SPAM) ---
    {
        "label_text": "spam",
        "text": """URGENT SECURITY ALERT: Your Microsoft 365 account has been temporarily restricted due to unauthorized login attempts. Please click here to verify your credentials and avoid permanent account termination within 24 hours: http://m365-security-check.com"""
    },
    {
        "label_text": "spam",
        "text": """Exclusive Crypto Investment Opportunity: Earn 300% weekly returns with our automated Bitcoin AI trading bot. Guaranteed payouts directly to your wallet. Deposit $500 today to start receiving daily dividends. Sign up here: http://crypto-wealth-secret.biz"""
    },

    # --- Legitimate Business & Email Correspondence (HAM) ---
    {
        "label_text": "ham",
        "text": """Hi team, Please find attached the updated quarterly financial report for review. We will walk through the budget allocations and expense forecasts during tomorrow morning's staff meeting at 10:00 AM. Let me know if you have any questions beforehand. Best regards, Sarah Jenkins"""
    },
    {
        "label_text": "ham",
        "text": """Dear John, Thanks for reaching out regarding our consulting services. I would be happy to schedule a 30-minute introductory call next Tuesday or Wednesday afternoon to discuss your company's requirements and see how we can assist. Does 2:00 PM EST work for your calendar? Looking forward to speaking with you. Warm regards, Michael"""
    },
    {
        "label_text": "ham",
        "text": """Good morning, Just following up on the design assets for the new landing page. Have the marketing and product teams signed off on the latest mockups? We are ready to begin the frontend implementation once we get the green light. Thanks, Alex"""
    },
    {
        "label_text": "ham",
        "text": """Hi David, Attached is the draft contract for the vendor agreement. Please review sections 4 and 7 regarding service level agreements and confidentiality before we send it over for signatures. Let me know if any amendments are needed. Regards, Lisa Chang, Legal Counsel"""
    },
    {
        "label_text": "ham",
        "text": """Hey everyone, Friendly reminder that the office will be closed on Monday for the national holiday. If you have urgent tasks that need deployment before then, please ensure PRs are merged by Friday 3 PM. Have a great weekend!"""
    },
    {
        "label_text": "ham",
        "text": """Dear Professor Thompson, I am writing to ask if you might have office hours this Thursday to discuss my research proposal on distributed systems. I have completed the preliminary literature review and would value your feedback on the methodology. Thank you for your time, Rachel"""
    },
    {
        "label_text": "ham",
        "text": """Hello Mark, Hope you are having a productive week. We have finalized the sprint planning for next cycle. The ticket priorities have been updated in Jira, and the backlog grooming is complete. Please let me know if you see any blockers. Thanks, Kevin"""
    },
    {
        "label_text": "ham",
        "text": """Hi Robert, Thanks for submitting your photography portfolio for our creative directory. Our editorial team reviewed the sample gallery and loved your architectural shots. We would like to feature two of them in next month's issue. Please let us know if you would be open to this collaboration. Best, Emily"""
    }
]
