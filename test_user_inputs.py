from predict import SpamClassifier

c = SpamClassifier()

msg1 = (
    "Hello,Greetings to you\"Thanks for your quick response.A top VIP in one of the African "
    "Countries is in dire need of anentrepreneur or fund manager that can confidently receive "
    "and manage thesum of US$5.2 Billion with a reasonable return on investment annually.Please "
    "should you find this offer interesting, kindly revert back to meso we can discuss modalities "
    "that will perfect the transfer of the fundsto any account you may deem safe.To make this happen, "
    "a meeting may be arranged where this transactionwill be discussed one on one and measures will "
    "be streamlined for asuccessful completion of the transaction where applicable.Note: For your "
    "eligibility to handle this significant huge funds, youwould have to own a company and operational "
    "bank account where the fundshall be transferred into for the investment purposes.Also, You must "
    "have a project plan to accommodate and invest the funds.Please feel free to contact me and i would "
    "be happy to provide furtherdetails.Regards,Mr. William Schneider"
)

msg2 = (
    "A top VIP in one of the African Countries is in dire need of anentrepreneur or fund manager "
    "that can confidently receive and manage thesum of US$5.2 Billion with a reasonable return on "
    "investment annually.Please should you find this offer interesting, kindly revert back to meso "
    "we can discuss modalities that will perfect the transfer of the fundsto any account you may deem safe."
)

for idx, m in enumerate([msg1, msg2], 1):
    r = c.predict(m)
    print(f"\n{'='*70}")
    print(f"Test Email #{idx}:")
    print(f"Prediction:     [{r['prediction']}]")
    print(f"Confidence:     {r['confidence'] * 100:.2f}%")
    print(f"Probabilities:  Ham: {r['ham_probability']*100:.2f}% | Spam: {r['spam_probability']*100:.2f}%")
    print("Scam Indicators Triggered:")
    for rule in r['triggered_rules']:
        print(f"  * {rule}")
print(f"{'='*70}\n")
