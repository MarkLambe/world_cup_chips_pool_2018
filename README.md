# world_cup_chips_pool_2018

A script to predict the best strategy for the following competition.

![Competition Rules](https://raw.githubusercontent.com/MarkLambe/world_cup_chips_pool_2018/master/competition_rules.png)

The results it produces after 5,000,000 loops are as follows.

| Team         |   Points   |
| ------------ | :--------: |
| England      | 63.9272208 |
| Senegal      | 55.292432  |
| Portugal     | 52.2885104 |
| Spain        | 51.186084  |
| Russia       | 50.4672024 |
| Uruguay      | 50.273464  |
| Belgium      |  49.58387  |
| Peru         | 49.518812  |
| France       | 48.2849664 |
| Japan        | 48.0062968 |
| Argentina    | 47.854282  |
| Croatia      | 45.086184  |
| Germany      | 42.9098832 |
| Denmark      | 42.7656432 |
| Morocco      | 42.129936  |
| Brazil       | 41.9802432 |
| Tunisia      | 40.9755588 |
| South Korea  | 40.7168608 |
| Serbia       | 39.369123  |
| Egypt        | 39.338985  |
| Australia    | 38.6985148 |
| Poland       | 38.302812  |
| Colombia     | 36.1157104 |
| Panama       |  33.42593  |
| Saudi Arabia |  32.63915  |
| Nigeria      | 31.535613  |
| Sweden       | 31.1283912 |
| Mexico       | 30.432088  |
| Iceland      | 30.395439  |
| Iran         | 30.281952  |
| Switzerland  | 30.080714  |
| Costa Rica   | 20.8145448 |

Which led me to placing the following entry.

| Team     |   Points   | Coins Bet |
| -------- | :--------: | :-------: |
| England  | 63.9272208 |     8     |
| Senegal  | 55.292432  |     8     |
| Portugal | 52.2885104 |     8     |
| Spain    | 51.186084  |     4     |
| Russia   | 50.4672024 |     1     |
| Uruguay  | 50.273464  |     1     |

The script will output intermediate results every 10% of the way to completion.

Known Issues:
It doesn't fall back to head to head if two teams draw in the group stage, it just picks one.


Tests:
Install pytest 
Run 'pytest {test_file}' i.e 'pytest test_script.py' from root of project
