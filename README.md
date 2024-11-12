# Whales Market - Pre Snipe Alert

## The Idea - Whales Market

The Whales Market platform is a DeFi protocol where you can buy and sell tokens before an airdrop has occured. While going through their smart contract transactions, I noticed that for the last few tokens that had been added there was a really odd arbitrage occuring. When a token was created it would call a specific createToken function with the new token id as a parameter. There is another function called newOffer where once a token is launched, users can create a new offer to potentially sell their token. For the past few tokens before I had coded this project, a few hours after a token was created, there would be a new offer of the same eth denomination that was a significant discount on the price of the token even a day later. Also, this offer was generally not being bought until a few hours later. So, I wanted to see if I could identify when a new token was created, and when the first offer was made on that token, so I could buy it at a discount and sell later.

## The Outcome

In the next couple of token launches following this project, the newOffers started to vary and were not at as much of a discount as the other ones I had noticed. This was a project in Februrary of 2024 so the protocol was still fairly new. Not sure exactly what the mechanism was that I had initially noticed. Maybe it was a way that the Whales Market team initially injected volume into the token for the first few launches. Nonetheless, the opportunity was not as apparant as time went on. Have not looked into it recently, but it may be an opportunity now that the Whales Market protocol more consistently launches tokens.
