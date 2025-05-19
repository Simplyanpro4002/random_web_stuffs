# Test questions with proper formatting
QUESTIONS = [
    {
        'id': 1,
        'narrative': r'''As you settle into Grandma Cat's old study, you discover her worn journal. Flipping through the pages, you find an old question scrawled in her pawwriting:
"Before a cat makes a move in the market, it's important to know how others see their instincts. The clowder never forgets…"
You think back to your fellow feline friends—those who've seen you leap, hide, and prowl.''',
        'question_text': 'How would your best cat friend describe your approach to risk?',
        'options': [
            ('a', "A real gambler — you leap before you even check where you'll land."),
            ('b', "A calculated climber — you study the bookshelf's height before the jump."),
            ('c', "Cautious — you sniff every corner before you make a move."),
            ('d', "A total risk avoider — if there's a shadow, you're under the couch.")
        ]
    },
    {
        'id': 2,
        'narrative': r'''The next page of the journal says:
"Sometimes things don't go as planned. What a cat does when their bowl runs empty says a lot about their comfort with uncertainty."
An old memory came to your mind. There was one time you saved up for a trip to the Clawibbean Isles. But just days before departure, you were fired from your job.''',
        'question_text': 'What did you do with your Clawibbean vacation plans?',
        'options': [
            ('a', "Canceled the trip — survival comes first."),
            ('b', "Took a more modest trip — something safe but relaxing."),
            ('c', "Went as scheduled — you earned it, and things will work out."),
            ('d', "Extended the trip — no job, no stress, time to live your best life")
        ]
    },
    {
        'id': 3,
        'narrative': r'''As you keep reading Grandma's journal, you noticed a word that was repeated multiple times - Risk.
"Every cat has a different reaction to the word," you remember her saying. "How you feel about risk shapes how you leap."''',
        'question_text': 'What comes to mind when you hear the word "risk"?',
        'options': [
            ('a', "Loss — it means giving up what you have."),
            ('b', "Uncertainty — anything could happen."),
            ('c', "Opportunity — it might lead to something better."),
            ('d', "Thrill — it gets your tail twitching in excitement.")
        ]
    },
    {
        'id': 4,
        'narrative': r'''You flip to the next page of Grandma's journal. Her pawwriting is a little more hurried, as if this entry came after a long night of trading tuna futures.
"Every cat thinks they understand risk — until the market shifts. That's when instincts speak loudest."
She writes about a moment in her own life, when whispers swirled through the clowder: real estate would be climbing, rare jewelry would be in demand, bond prices would fall, but government bonds are relatively safe.
You blink. That's familiar. Right now, most of your savings are sitting in those high-interest government bonds. The thought of shaking things up unsettles your fur.
"When the winds change," Grandma wrote, "do you plant your paws… or leap?"''',
        'question_text': 'What would you do in this situation?',
        'options': [
            ('a', "Hold the bonds"),
            ('b', "Sell the bonds, put half the proceeds into money market accounts, and the other half into hard assets"),
            ('c', "Sell the bonds and put the total proceeds into hard assets"),
            ('d', "Sell the bonds, put all the money into hard assets, and borrow additional money to buy more")
        ]
    },
    {
        'id': 5,
        'narrative': r'''"Growth may outpace the slow crawl of inflation, but it comes with storms. Stability protects your fur in rough weather, but may leave you behind."
You pause and consider what kind of hunter you are—or want to be.''',
        'question_text': 'Thinking about how your pawfolio might grow over time, which approach fits your goal best?',
        'options': [
            ('a', "I want my investments to be calm and steady, even if they don't always catch up with the rising cost of catnip."),
            ('b', "I prefer a balance—some growth with modest ups and downs, enough to keep up with inflation."),
            ('c', "I aim for growth that beats inflation, even if it means riding some bigger waves."),
            ('d', "I'm ready to chase the biggest leaps, accepting larger swings for the chance of great rewards.")
        ]
    },
    {
        'id': 6,
        'narrative': r'''The last folded page of Grandma's journal notes:
"Gold is heavy, but decisions are heavier. Especially when it's your friend who asks you to dig."
You close the journal and look out the window, where your longtime neighbor, Marmalade, is pacing in his yard. You've known him forever. He's an expert on underground things: gems, geology, gossip. And now, he's raising funds for a new gold mining venture in the southern cliffs.
He says the payout could be huge — 50 to 100 times your investment — but there's only a 1-in-5 chance of success. If it flops, you lose it all.''',
        'question_text': "How much would you invest in Marmalade's risky but promising venture?",
        'options': [
            ('a', "Nothing — a 20% chance isn't worth losing my fur over."),
            ('b', "A modest sum — maybe a month's salary, just to see."),
            ('c', "A more serious stake — three months' salary if the gut says go."),
            ('d', "Half a year's salary — big risk, big reward, big tail twitch.")
        ]
    },
    {
        'id': 7,
        'narrative': r'''With Grandma's journal closed for now, you step outside into the bustling alleys of Meowpolis. The world of investments is no longer just words on a page — it's time to make your first real moves.
The first portion of your inheritance was given to you - $20,000.''',
        'question_text': 'What do you decide to do with the $20,000?',
        'options': [
            ('a', "Curl up safely in the bank's Deposit Den — guaranteed protection, slow growth."),
            ('b', "Place it in stable bonds, like Fishback Bonds — steady, with some interest, fewer surprises."),
            ('c', "Venture into stocks or mutual funds — riskier, but with the chance to grow much more.")
        ]
    },
    {
        'id': 8,
        'narrative': r'''Having made your first choice with the $20,000 inheritance, you wander through the vibrant Market District of Meowpolis.
At the bustling Market Square, you bump into an old investor cat, who is your grandma's old friend. He chuckles, showing you his collection of stock certificates and trading cards.
"So, young paw, how comfy are you with the wild world of stocks? It's a jungle out there—sometimes purrfect, sometimes perilous."''',
        'question_text': 'How will you answer him?',
        'options': [
            ('a', "Not at all — the thought of those ups and downs makes my fur stand on end."),
            ('b', "Somewhat — I'm curious and willing to explore, but I watch my step carefully."),
            ('c', "Very — I'm ready to pounce on opportunities, even if it means a few scratches along the way.")
        ]
    },
    {
        'id': 9,
        'narrative': r'''After your chat with the old cat in the Market Square, he paws you a worn booklet. "This," he purrs, "is the Ledger of Legendary Investments — a collection of true tales from the boldest cats in Meowpolis. Flip through, and see what kind of investor you are."
Inside, four faded stories catch your eye. Each tells of a different cat and the outcome of their boldest leap. Some landed gracefully. Others… not so much.
Whiskerstein asks, "If you had to pick one of these paths — knowing what you might gain or lose — which feels the most like you?"''',
        'question_text': 'Choose the investment tale that best fits your appetite for risk and reward:',
        'options': [
            ('a', "The Safe Stash — gained $200, risked nothing."),
            ('b', "The Balanced Pounce — gained $800, risked $200."),
            ('c', "The Big Stretch — gained $2,600, risked $800."),
            ('d', "The Daring Leap — gained $4,800, risked $2,400.")
        ]
    },
    {
        'id': 10,
        'narrative': r'''After a long day at the market, you returned home. Waiting for you was a delivery package from Grandma's lawyer.
Inside lies a crisp letter, paw-signed by Grandma herself. It reads:
"Each of you seven grandkittens will face a moment of truth. To claim the full inheritance, you must prove who you are with your investment choices. One decision, one direction. No hedging your tail."
A note is attached with a final challenge:
"Here is $100,000. Choose one way to invest it. Choose wisely."''',
        'question_text': 'How would you invest your 100,000 inheritance from Grandma Purrl?',
        'options': [
            ('a', "In the Snuggle Bank — a safe savings account or money market fund. Calm, cool, and curl-up secure."),
            ('b', "In a Balanced Fund Basket — a gentle mix of stocks and bonds. Not too hot, not too cold."),
            ('c', "In the Claw Street Collection — 15 carefully chosen common stocks. All in on growth."),
            ('d', "In the Glittering Den — raw goods like gold, silver, and oil. Tangible, volatile, and untamed.")
        ]
    },
    {
        'id': 11,
        'narrative': r'''Just as you thought that was everything, you hear a soft "thunk" — a smaller envelope slides out of the larger package. It's marked with a paw-embossed seal and a faint scent of catnip cookies.
You tear it open, and inside is a shorter letter. Grandma's writing is shakier, but just as firm:
"One big decision shows your claws. But real investing? That's in the details. If you had $20,000 instead — not for one path, but for many — how would you divide them?"''',
        'question_text': 'What would be your answer?',
        'options': [
            ('a', "60% low-risk, 30% medium-risk, 10% high-risk — You'd rather nap than leap without a net."),
            ('b', "30% low-risk, 40% medium-risk, 30% high-risk — A prowling planner with curiosity and claws."),
            ('c', "10% low-risk, 40% medium-risk, 50% high-risk — You're ready to hunt where others hesitate.")
        ]
    },
    {
        'id': 12,
        'narrative': r'''A few days later, you found another letter in your mail box, sent from Grandma's lawyer. It was a sealed envelope pawmarked by Grandma herself.
"You've been awarded 1,000 whisker-coins for your progress so far," it reads.
"Now choose how you want to receive this gift."''',
        'question_text': 'You must decide:',
        'options': [
            ('a', "Take a guaranteed $500. Safe, soft, and sure."),
            ('b', "Take a 50/50 chance: either receive the full $1,000… or nothing at all.")
        ]
    },
    {
        'id': 13,
        'narrative': r'''Just as you think the journey is over, the markets of Meow Street — once booming — now down 20% in just a whisker's time.''',
        'question_text': 'If your portfolio dropped by 20% in a short stretch of moon cycles, how would you respond?',
        'options': [
            ('a', "Stay the course — no change. Grandma rode storms, and so will I."),
            ('b', "Wait a full year before shifting toward safer nests — things might bounce back."),
            ('c', "Wait three moons (months), then consider retreating to more padded pawsitions."),
            ('d', "Retreat now — shift everything to safe napping nests. No more surprises.")
        ]
    },
    {
        'id': 14,
        'narrative': r'''Your holdings have earned a bonus of $2,000. To process your reward, a service fee must be paid.''',
        'question_text': 'You must decide how to handle this fee:',
        'options': [
            ('a', "Pay a guaranteed $500 — a sure, fixed toll to receive your reward."),
            ('b', "Take a chance on the fee: a 50% chance to pay $1,000, or a 50% chance to pay nothing at all.")
        ]
    },
    {
        'id': 15,
        'narrative': r'''After all the choices, tests, and twists, your journey leads you to the meeting of the 7 heirs with Grandma's lawyer, who was entrusted by her to assess her heirs.
The seven grandkittens gather in the grand hall, the air thick with excitement and a hint of friendly rivalry. The lawyer cat steps forward, holding the final challenge in his paws.
"To prove your true investment spirit, each of you must make one last choice. The prize is yours to claim — but the path you pick will say much about your courage and wisdom."''',
        'question_text': 'Which prize do you choose?',
        'options': [
            ('a', 'A guaranteed $1,000 — steady and sure, like a warm spot by the fire.'),
            ('b', "A 50% chance to win $5,000 — a tempting leap with hopeful paws."),
            ('c', "A 25% chance to win $10,000 — a bolder prowl for greater rewards."),
            ('d', "A daring 5% chance to win $100,000 — the wildest chase for the bravest of hearts.")
        ]
    }
] 