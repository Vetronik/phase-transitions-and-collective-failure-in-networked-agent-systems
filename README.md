# When Communication Amplifies Error

**Can a group agree on an answer and still be wrong?** This research project explores how communication can help a group make better decisions—and how it can also spread a shared mistake.

Created by **Veronika Loran**, the project contains a research paper, computer simulations, and the results behind the paper. Its repository name is *Phase Transitions and Collective Failure in Networked Agent Systems*.

## The idea in everyday language

Imagine asking a group of people whether a statement is true. Each person has a clue, but some clues are wrong. If their clues come from different sources, comparing answers can help the group reach the right conclusion.

Now imagine that many people got their clue from the same unreliable source. As they repeat each other's answers, the same mistake may start to sound like confirmation from several independent sources. The group can become almost unanimous while being wrong.

This project studies that possibility in a simplified computer experiment.

## How the study works

The simulations use virtual decision-makers called **agents**. Each agent chooses between two answers, receives an imperfect clue, and can be influenced by connected neighbors. The correct answer is known, so the experiment can measure whether communication helps.

The study changes how reliable the clues are, how much they share a common source of error, and how strongly agents influence one another. It measures correctness, agreement, and how often most of the group ends up wrong.

## What the results show

In one main experiment with 256 agents, each agent's initial clue had a 55% chance of being correct. With strong communication:

| Where the clues came from | Average individual accuracy after communication |
| --- | --- |
| Independent sources | About 95% |
| Sources with some shared errors | About 40% |

Both groups reached almost complete agreement. These particular results illustrate the central finding: **agreement alone does not tell us whether a group is right.**

A separate experiment found that strong mutual influence could make a large group behave, in terms of its errors, roughly like a single decision-maker. More agents then added little independent information.

## What these findings mean

The study gives a controlled example of why the independence of information matters when evaluating a group's decisions. It may help frame questions about teamwork, online communities, and collaborating AI systems.

These are results from a simplified mathematical model, with limited numbers of repeated experiments. The study does not directly test people or language models, and its percentages should not be treated as predictions for real-world groups.

Although the repository name mentions “phase transitions,” the current evidence does **not** establish a true phase transition—a lasting, abrupt change in behavior as the system becomes very large.

## Explore the project

No coding is needed to read the paper or browse the findings.

- **Read the paper:** [PDF](paper/main.pdf) or [Word document](paper/main.docx).
- **Browse the main findings:** [Results summary](analysis/results_summary.md).
- **See the charts:** [Figures](results/figures/).
- **Understand the scope:** [Central research claim](protocol/central_claim.md) and the limitations discussed in the paper.
- **Explore the research materials:** [Simulation code](src/collective_agents/), [experiment settings](configs/), and [recorded results](results/).

For readers who want to rebuild the paper, see the [manuscript instructions](paper/README.md).
