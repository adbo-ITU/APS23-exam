#include <climits>
#include <iostream>
#include <map>
#include <queue>
#include <vector>

#define vertex tuple<int, int, int>
#define flow_graph map<vertex, map<vertex, int>>

using namespace std;

const int IN_FLAG = 0, OUT_FLAG = 1;
const int DIRECTIONS[] = {-1, 0, 1};
const vertex SOURCE = {-1, 0, OUT_FLAG};
const vertex SINK = {-1, 1, IN_FLAG};

// Breadth-first search
pair<bool, vector<pair<vertex, vertex>>> find_path(flow_graph& graph, int min_capacity) {
    map<vertex, vertex> parent;
    queue<vertex> q;
    q.push(SOURCE);

    while (!q.empty()) {
        auto u = q.front();
        q.pop();

        for (auto const& [v, capacity] : graph[u]) {
            if (capacity <= min_capacity || parent.find(v) != parent.end()) {
                continue;
            }

            parent[v] = u;
            q.push(v);

            if (v == SINK) {
                vector<pair<vertex, vertex>> path;
                for (auto current = v; current != SOURCE; current = parent[current]) {
                    path.emplace_back(parent[current], current);
                }
                return {true, path};
            }
        }
    }

    return {false, {}};
}

int find_max_flow(const flow_graph& original_graph) {
    flow_graph graph;
    int max_capacity = 0;

    for (auto const& [from, tos] : original_graph) {
        for (auto const& [to, capacity] : tos) {
            graph[from][to] = capacity;
            max_capacity = max(max_capacity, capacity);
        }
    }

    int current_flow = 0;
    int min_capacity = max_capacity;

    while (true) {
        auto [has_path, path] = find_path(graph, min_capacity);

        if (!has_path) {
            if (min_capacity <= 0)
                return current_flow;

            min_capacity /= 2;
            continue;
        }

        int path_flow = INT_MAX;
        for (auto const& [u, v] : path) {
            path_flow = min(path_flow, graph[u][v]);
        }
        current_flow += path_flow;

        for (auto const& [u, v] : path) {
            graph[u][v] -= path_flow;
            graph[v][u] += path_flow;
        }
    }
}

int main() {
    int r, c, b;
    cin >> r >> c >> b;

    map<vertex, map<vertex, int>> graph;
    vector<vector<bool>> grid(r, vector<bool>(c, false));

    // Read input
    string line;
    for (int row = 0; row < r; ++row) {
        cin >> line;
        for (int col = 0; col < c; ++col)
            grid[row][col] = line[col] == '#';
    }

    // Construct graph
    for (int row = 0; row < r; ++row) {
        for (int col = 0; col < c; ++col) {
            if (!grid[row][col])
                continue;

            graph[{row, col, IN_FLAG}][{row, col, OUT_FLAG}] = 1;

            for (int dy : DIRECTIONS) {
                for (int dx : DIRECTIONS) {
                    if (dy == 0 && dx == 0)
                        continue;

                    int y = row + dy, x = col + dx;
                    if (y < 0 || y >= r || x < 0 || x >= c || !grid[y][x])
                        continue;

                    graph[{row, col, OUT_FLAG}][{y, x, IN_FLAG}] = 1;
                }
            }
        }
    }

    // Add source and sink
    for (int col = 0; col < c; ++col) {
        if (grid[0][col]) {
            graph[SOURCE][{0, col, IN_FLAG}] = 1;
        }
        if (grid[r - 1][col]) {
            graph[{r - 1, col, OUT_FLAG}][SINK] = 1;
        }
    }

    int max_flow = find_max_flow(graph);
    cout << max(0, b - max_flow) << endl;

    return 0;
}
