import java.util.ArrayList;
import java.util.Arrays;
import java.util.Random;

/**
 * Created by paulpm on 22/10/15.
 */
public class Board {

    // PROPERTIES

    private int[][] grid = new int[][]{
            {0, 0, 0, 0},
            {0, 0, 0, 0},
            {0, 0, 0, 0},
            {0, 0, 0, 0},
    };
    private int score;


    // CONSTRUCTOR

    public Board() {
        placeRandomTile();
        score = 0;
    }

    public Board(int[][] grid, int score) {
        this.grid = grid;
        this.score = score;
    }

    // PLACEMENT METHODS

    public void placeRandomTile() {
        ArrayList<Coordinate> freeSlots = getFreeTiles();
        if (freeSlots.size() > 0) {
            int randomCoordinateIndex = new Random().nextInt(freeSlots.size());
            Coordinate coordinate = freeSlots.get(randomCoordinateIndex);
            placeTile(coordinate, new Random().nextDouble() < 0.9 ? 2 : 4);
        }
    }

    public void placeTile(Coordinate coordinate, int tile){
        grid[coordinate.getX()][coordinate.getY()] = tile;
    }

    public void placeTile(int x, int y, int tile){
        grid[x][y] = tile;
    }

    public ArrayList<Coordinate> getFreeTiles(){
        ArrayList<Coordinate> freeTiles = new ArrayList<>();
        for (int x = 0; x < 4; x++){
            for (int y = 0; y < 4; y++){
                if (grid[x][y] == 0){
                    freeTiles.add(new Coordinate(x,y));
                }
            }
        }
        return freeTiles;
    }

    // MOVEMENT METHODS

    public boolean moveLeft(){
        boolean moved = false;
        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++) {
                if (grid[x][y] != 0) {
                    for (int z = y; z < 4; z++) {
                        if (grid[x][y] == grid[x][z] && y != z){
                            int tile = grid[x][y] * 2;
                            placeTile(x, y, tile);
                            placeTile(x, z, 0);
                            setScore(getScore() + tile);
                            moved = true;
                            break;
                        }
                        if (grid[x][z] != 0 && grid[x][y] != grid[x][z]) {
                            break;
                        }

                    }
                }
            }
        }

        for (int x = 0; x < 4; x++) {
            for (int y = 0; y < 4; y++){
                if (grid[x][y] == 0) {
                    for (int z = y; z < 4; z++) {
                        if (grid[x][z] != 0) {
                            placeTile(x, y, grid[x][z]);
                            placeTile(x, z, 0);
                            moved = true;
                            break;
                        }
                    }
                }
            }
        }
        return moved;
    }

    public boolean moveUp(){
        boolean moved = false;

        for (int y = 0; y < 4; y++) {
            for (int x = 0; x < 4; x++) {
                if (grid[x][y] != 0) {
                    for (int z = x; z < 4; z++) {
                        if (grid[z][y] != 0 && x != z)
                            if (grid[z][y] != 0 && grid[z][y] != grid[x][y]){
                                break;
                            }
                        if (grid[x][y] == grid[z][y] && x != z){
                            int tile = grid[x][y] * 2;
                            placeTile(x, y, tile);
                            placeTile(z, y, 0);
                            setScore(getScore() + tile);
                            moved = true;
                            break;
                        }
                    }
                }
            }
        }

        for (int y = 0; y < 4; y++) {
            for (int x = 0; x < 4; x++) {
                if (grid[x][y] == 0) {
                    for (int z = x; z < 4; z++) {
                        if (grid[z][y] != 0){
                            placeTile(x, y, grid[z][y]);
                            placeTile(z, y, 0);
                            moved = true;
                            break;
                        }
                    }
                }
            }
        }
        return moved;
    }

    public boolean moveRight(){
        boolean moved;
        reverseLeftRight();
        moved = moveLeft();
        reverseLeftRight();
        return moved;
    }

    public boolean moveDown(){
        boolean moved;
        reverseUpDown();
        moved = moveUp();
        reverseUpDown();
        return moved;
    }

    private void reverseLeftRight(){
        for (int[] elem : grid){
            for (int i = 0; i < elem.length / 2; i++) {
                int temp = elem[i];
                elem[i] = elem[elem.length - i - 1];
                elem[elem.length - i - 1] = temp;
            }
        }
    }

    private void reverseUpDown(){
        for (int i = 0; i < grid.length / 2; i++){
            int[] temp = grid[i];
            grid[i] = grid[grid.length - i - 1];
            grid[grid.length - i - 1] = temp;
        }
    }

    public boolean move(Direction direction) {
        boolean moved = false;

        switch (direction) {
            case DOWN:
                moved = moveDown();  break;
            case UP:
                moved = moveUp();    break;
            case LEFT:
                moved = moveLeft();  break;
            case RIGHT:
                moved = moveRight(); break;

        }
        return moved;

    }

    public boolean isAvailableMoves() {

        Board copy = copy();
        if (copy.moveDown() || copy.moveUp() || copy.moveLeft() || copy.moveRight()) {
            return true;
        }

        return false;
    }


    // GETTERS & SETTERS

    public int[][] getGrid() {
        return grid;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

    public Board copy() {
        int[][] copy = new int[getGrid().length][getGrid().length];
        for (int i = 0; i < copy.length; i++){
            for (int j = 0; j < copy.length; j++){
                copy[i][j] = getGrid()[i][j];
            }
        }
        return new Board(copy, score);
    }

    public String toString() {
        String board = "";
        for(int x = 0; x<4; x++){
            board += Arrays.toString(grid[x]) + "\n";
        }
        board += "\n-------------------------------------";
        return board;
    }
}
