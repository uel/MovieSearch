#include <fstream>
#include <sstream>
#include <vector>
#include <sstream>
#include <unordered_map>
using namespace std;

struct Node
{
    uint32_t doc_id;
    float weight;
};

unordered_map<string, int> LoadMap(string filename)
{
    unordered_map<string, int> map;
    ifstream file(filename);
    string line;
    while (getline(file, line))
    {
        string key;
        int value;
        stringstream ss(line);
        ss >> key >> value;
        map[key] = value;
    }
    file.close();
    return map;
}

vector<string> LoadLines(string filename)
{
    vector<string> lines;
    ifstream file(filename);
    string line;
    while (file >> line) lines.push_back(line);
    file.close();
    return lines;
}

void SaveMap(string filename, unordered_map<string, int> map)
{
    ofstream file(filename);
    for ( auto i : map )
        file << i.first << "\t" << i.second << "\n";
    file.close();
}
