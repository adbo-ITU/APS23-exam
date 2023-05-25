#include <algorithm>
#include <iostream>
#include <set>
#include <vector>

using namespace std;

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;

    int s, f;
    vector<pair<int, int>> activities;
    for (int i = 0; i < n; i++) {
        cin >> s >> f;
        activities.emplace_back(s, f);
    }

    // Sort activities by finish time, then by start time
    sort(activities.begin(), activities.end(),
        [](pair<int, int> left, pair<int, int> right) {
            if (left.second == right.second) {
                return left.first < right.first;
            } else {
                return left.second < right.second;
            }
        }
    );

    // Set the initial ending times of the classrooms to 0
    multiset<int> classrooms;
    for (int i = 0; i < k; i++) {
        classrooms.insert(0);
    }

    int max_activities = 0;
    for (auto [s, f] : activities) {
        auto it = classrooms.upper_bound(-s);

        // If a classroom is available, use it
        if (it != classrooms.end()) {
            classrooms.erase(it);
            classrooms.insert(-f);
            max_activities++;
        }
    }

    cout << max_activities << endl;
    return 0;
}
