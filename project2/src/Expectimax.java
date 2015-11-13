/**
 * Created by paulpm on 22/10/15.
 */
public class Expectimax {

    private static final int DEPTH = 5;
    private static final int[][] WEIGHT_MATRIX = new int[][]{
            {0,1,2,3},
            {6,5,5,4},
            {7,9,12,15},
            {55,35,25,20}
    };


    private Board board;

    public Expectimax(Board board) {
        this.board = board;
    }

    /**
     * Calculates which direction the AI should move in order to maximize it's potential score.
     * @param board - A Board object on which to base the calculation
     * @param depth - Integer representing the number of steps to look ahead. Current capacity seems to be 6,
     *                however with dynamic depth we can increase the depth to 8 when there are fewer free tiles
     *                (because fewer empty tiles = smaller search tree.)
     * @return A direction to move (up, down, left, right).
     */
    private Direction recommendMove(Board board, int depth) {
        double maxScore = Double.NEGATIVE_INFINITY;
        Direction bestDirection = Direction.DOWN;

        for (Direction direction : Direction.values()) {
            Board copy = board.copy();
            if (copy.move(direction)) {
                double currentScore = expectimax(copy, depth );
                if (currentScore > maxScore) {
                    maxScore = currentScore;
                    bestDirection = direction;
                }
            }
        }
        return bestDirection;
    }
    /**
     * Expectimax algorithm. If we, the AI player, are to play at node (e.g. if the depth of the search tree
     * is even), we check which of the four directions will yield the highest score if moved to. Otherwise,
     * if we are at a CHANCE node (e.g. if the depth of the search tree is odd), we calculate the weighted
     * average of all child node's values. There will be (2 * number of empty tiles) board copies generated.
     * @param board - A Board object on which to apply the expectimax algorithm
     * @param depth - Integer representing the number of steps to look ahead
     * @return The expected maximum value of a move
     */
    public double expectimax(Board board, int depth) {
        double score = Double.NEGATIVE_INFINITY;
        if (depth == 0) {
            return !board.isAvailableMoves() ? score : calculateUtility(board);
        }
        else if (depth % 2 == 0) {
            for (Direction direction : Direction.values()) {
                Board copy = board.copy();
                if (copy.move(direction)) {
                    score = Math.max(score, expectimax(copy, depth - 1));
                }
            }
        }
        else if (depth % 2 == 1) {
            score = 0;
            for (Coordinate coordinate : board.getFreeTiles()) {
                Board alpha = board.copy();
                Board beta = board.copy();
                alpha.placeTile(coordinate, 2);
                beta.placeTile(coordinate, 4);
                score += 0.9 * expectimax(alpha, depth - 1);
                score += 0.1 * expectimax(beta, depth - 1);
            }
            score = score / board.getFreeTiles().size();
        }
        return score;
    }

    /**
     * Calculates the score of any given state based on the Snake Pattern approach (as represented in the
     * WEIGHT_MATRIX property.
     * @param node - A Board object (state) on which to calculate the heuristic for.
     * @return The score of the current board based on the Snake Pattern heuristic.
     */
    private double calculateUtility(Board node) {

        double value = 0;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                value += node.getGrid()[i][j]*WEIGHT_MATRIX[i][j]*2;
            }
        }
        return value;
    }



    /**
     * AI plays 2048. First retrieve the best direction to move given the current state, and dynamically look ahead
     * further in the search tree if there are fewer than three empty tiles left. We then update the board by moving
     * to the given direction, and then we place a random tile in a random location in the grid.
     */
    public void run() {
        Board board = getBoard();

        Direction bestDirection = board.getFreeTiles().size() < 4
                ? recommendMove(board, DEPTH + 2)
                : recommendMove(board, DEPTH);

        board.move(bestDirection);
        board.placeRandomTile();
    }


    /**
     * Gets the board
     * @return A Board object
     */
    public Board getBoard() {
        return board;
    }
}
