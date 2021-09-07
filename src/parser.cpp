#include<iostream>
#include<fstream>
#include<sstream>
#include <vector>

using namespace std;

bool is_number(const string& s)
{
    string::const_iterator it = s.begin();
    while (it != s.end() && (isdigit(*it) || isspace(*it))) ++it;
    return !s.empty() && it == s.end();
}

int main()
{
    ifstream input;
    input.open("../test2/web-NotreDame.txt");
    ofstream output("../test2/web-NotreDame.grf");
    string line;
    int tail = 0;
    vector<string> heads;
    int count = 0;

    if (input.is_open())
    {
        int max = -1;
        while(!input.eof() )
        {
            getline(input, line);
            stringstream iss(line);
            int idx;
            while (iss >> idx)
                if (idx > max)
                    max = idx;
        }
        output << max+1;
        output << '\n';
        for (int i = 0; i <= max; i++)
        {
            output << i;
            output << '\n';
        }
        input.clear();
        input.seekg(0, input.beg);

        while (!input.eof())
        {
            getline(input, line);
            if (!is_number(line))
                continue;

            stringstream iss(line);
            int idx;
            vector<int> edge;
            while (iss >> idx)
                edge.push_back(idx);

            if (edge[0] > tail)
            {                        
                output << heads.size();
                output << "\n";
                for (vector<string>::iterator it = heads.begin(); it != heads.end(); ++it)
                    output << *it;
                heads.clear();

                for (int j = 1; j <= edge[0]-tail-1; j++)
                    output << "0\n";

                tail = edge[0];
            }
            heads.push_back(line);
            count++;
        }

        if (!heads.empty())
            {
                output << heads.size();
                output << "\n";
                for (vector<string>::iterator it = heads.begin(); it != heads.end(); ++it)
                    output << *it;
                count++;
            }
    }
    input.close();
    output.close();
    return 0;
}