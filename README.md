# Chess game in python / Pygame

## Goal
- [x] First basic UI with PVP (tag 1.0)
- [x] Simplistic AI (Random AI)
- [x] AI vs AI (tag 2.0)
- [X] Basic AI (simple board evaluation based on pieces)
- [ ] Basic Min-Max (simple board evaluation in a Min-Max algo)
- [ ] Others improvements (alpha pruning, heatmap, pawn structure ...)



## Some stats
After 200 games between 2 __random__ AIs

|  Game Result                       |  nb   |   %    |
| ---------------------------------- | ----- | ------ |
| White wins                         |  22   |  11%   |
| Black wins                         |  20   |  10%   |
| Null: Draw by 50-Move Rule         |  97   |  48.5% |
| Null: Draw by Dead Position        |  34   |  17%   |
| Null: Stalemate                    |  24   |  12%   |
| Null: Draw by Threefold Repetition |   3   |   1.5% |


After 200 games between 2 __basic__ AIs

|  Game Result                       |  nb   |   %    |
| ---------------------------------- | ----- | ------ |
| White wins                         |   4   |   2%   |
| Black wins                         |   1   |   0.5% |
| Null: Draw by Dead Position        | 136   |  68%   |
| Null: Draw by 50-Move Rule         |  37   |  18.5% |
| Null: Draw by Threefold Repetition |  15   |   7.5% |
| Null: Stalemate                    |   7   |   3.5% |

After 200 games between __basic__ (White) and __random__ (Black)  
__basic__ _wins 19%_ loses 0% null 81%

|  Game Result                       |  nb   |   %    |
| ---------------------------------- | ----- | ------ |
| White wins                         |  38   |  19%   |
| Black wins                         |   0   |   0%   |
| Null: Stalemate                    | 113   |  56%   |
| Null: Draw by 50-Move Rule         |  36   |	18%   |
| Null: Draw by Dead Position        |  10   |   5%   |
| Null: Draw by Threefold Repetition |   3   |   1.5% |

After 200 games between __random__ (White) and __basic__ (Black)  
__basic__ _wins 19%_ loses 0% null 81%

|  Game Result                       |  nb   |   %    |
| ---------------------------------- | ----- | ------ |
| White wins                         |   0   |   0%   |
| Black wins                         |  38   |  19%   |
| Null: Stalemate                    | 112   |  56%   |
| Null: Draw by 50-Move Rule         |  34   |  17%   |
| Null: Draw by Dead Position        |  14   |   7%   |
| Null: Draw by Threefold Repetition |   2   |   1%   |

