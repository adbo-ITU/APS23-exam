import java.util.Scanner;

public class Greedy {
    private final int r, c;
    private final boolean[][] grid, visited;
    private final static Direction[] directions = {
        new Direction(1, 0),   // Down
        new Direction(1, 1),   // Down right
        new Direction(0, 1),   // Right
        new Direction(-1, 1),  // Up right
        new Direction(-1, 0),  // Up
        new Direction(-1, -1), // Up left
        new Direction(0, -1),  // Left
        new Direction(1, -1),  // Down left
    };

    public Greedy(int r, int c) {
        this.r = r;
        this.c = c;
        this.grid = new boolean[r][c];
        this.visited = new boolean[r][c];
    }

    private void readGrid(Scanner sc) {
        for (int i = 0; i < grid.length; i++) {
            String row = sc.next();
            for (int j = 0; j < grid[i].length; j++) {
                grid[i][j] = row.charAt(j) == '#';
            }
        }
    }

    private int leftTurn(int direction, int steps) {
        return (direction + steps) % 8;
    }

    public boolean greedySearch(int row, int col, int direction) {
        // Out of bounds
        if (row < 0 || row >= r || col < 0 || col >= c) {
            return false;
        }
        // Already visited or not traversable
        if (visited[row][col] || !grid[row][col]) {
            return false;
        }

        visited[row][col] = true;

        // Path found
        if (row == r - 1) {
            return true;
        }

        // 180-degree turn
        direction = leftTurn(direction, 4);

        // Then explore all directions in a counter-clockwise manner
        for (int i = 0; i < directions.length; i++) {
            direction = leftTurn(direction, 1);
            int dy = directions[direction].dy;
            int dx = directions[direction].dx;

            if (greedySearch(row + dy, col + dx, direction)) {
                return true;
            }
        }

        return false;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int r = sc.nextInt(), c = sc.nextInt(), b = sc.nextInt();

        Greedy greedy = new Greedy(r, c);
        greedy.readGrid(sc);

        int paths = 0;
        for (int i = 0; i < c; i++) {
            if (greedy.greedySearch(0, i, 0)) {
                paths++;
            }
        }
        System.out.println(Math.max(0, b - paths));
    }

    private static class Direction {
        private final int dy, dx;

        public Direction(int dy, int dx) {
            this.dy = dy;
            this.dx = dx;
        }
    }
}
