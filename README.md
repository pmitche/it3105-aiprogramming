# IT3105 Artificial Intelligence Programming
Repository for hosting deliverables in the course IT3105 Artificial Intelligence Programming at the Norwegian University of Science and Technology, fall 2015. Entire course completed as a group effort with [Sondre Dyvik](https://github.com/sondrehd).

###### Project 1 - Implemented in Python 2.7
**module1:** Using A* to solve Navigation Problems.

**module2:** A*-GAC, A General Constraint-Satisfaction Problem Solver.

**module3:** Using A*-GAC to Solve Nonograms.

---


###### Project 2 - Implemented in Java using the [course-provided GUI](https://github.com/jorgenkg/IT3105)
**module4:** Minimax for Playing the 2048 Game.

Out of ten runs per heuristic, we achieved the following results:

| Heuristic     | 1024 tile     | 2048 tile  | 4096 tile | Average score | Best score |
| ------------- |:-------------:|:----------:|:---------:|:-------------:|:----------:|
| Snake         | 100%          | 100%       | 70%       | 55158         | 79472      |
| Gradient      | 100%          | 90%        | 50%       | 48206         | 76756      |
*See the report in the [project 2 directory](https://github.com/pmitche/it3105-aiprogramming/tree/master/project2) for more details.*

---


###### Project 3 - Implemented in Python 3.4 using [Theano](http://deeplearning.net/software/theano/)
**module5:** Neural Networks for Image Classification

Five different neural networks were tested on the MNIST dataset, and we achieved the following results:

| Neural net | Minibatch size | Epochs | Learning rate    | Training set average | Test set average | Average time trained |
| ---------- |:--------------:|:------:|:----------------:|:--------------------:|:----------------:|:--------------------:|
| Net #1     | 10             | 30     | 10<sup>-2</sup>  | 99.16%               | 97.71%           | 263.57 s             |
| Net #2     | 100            | 25     | 10<sup>-2</sup>  | 99.74%               | 97.95%           | 131.48 s             |
| Net #3     | 15             | 30     | 5*10<sup>-2</sup>| 99.73%               | 97.64%           | **95.91 s**          |
| Net #4     | 20             | 30     | 10<sup>-2</sup>  | **99.81%**           | **98.10%**       | 463.20 s             |
| Net #5     | 15             | 20     | 10<sup>-2</sup>  | 98.31%               | 97.34%           | 244.96 s             |
*See the module 5 report in the [project 3 directory](https://github.com/pmitche/it3105-aiprogramming/tree/master/project3) for more details.*

**module6:** Neural Networks for Game Playing

---

#### Licence
See the [LICENCE](https://github.com/pmitche/it3105-aiprogramming/blob/master/LICENCE.md) file for license rights and limitations (MIT).
