#include <iostream>
#include <math.h>
#include <vector>
#include <algorithm>
#include <set>
#include <map>
using namespace std;

void printLine()
{
    for (int i = 0; i < 100; i++)
    {
        cout << "-";
    }
    cout << "\n";
}

void UserInput(string &key, string &text)
{
    cout << "Enter The Key : \n";
    cin >> key;
    cout << "Enter The Text : \n";
    cin >> text;
    printLine();
}

string RemoveSpaces(string text)
{
    string res;
    for (auto x : text)
    {
        if (x == ' ')
            continue;
        res += x;
    }
    return res;
}

void replaceStringJ(string &str)
{
    for (auto &x : str)
    {
        if (x == 'j')
            x = 'i';
    }
}

void Encryption()
{
    string text, key;
    UserInput(key, text);
    text = RemoveSpaces(text);
    key = RemoveSpaces(key);
    replaceStringJ(key);
    replaceStringJ(text);
    transform(key.begin(), key.end(), key.begin(), ::tolower);
    transform(text.begin(), text.end(), text.begin(), ::tolower);

    // store the char in mat
    vector<vector<char>> matrix(5, vector<char>(5));

    set<char> keySet, remSet;
    bool isFind = true;
    for (int i = 0; i < 26; i++)
    {
        remSet.insert(i + 'a');
    }
    remSet.erase('j');
    for (auto x : key)
    {
        remSet.erase(x);
    }
    auto iter1 = 0;
    auto iter2 = remSet.begin();

    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            if (isFind)
            {
                while (iter1 < key.size() && keySet.count(key[iter1]))
                {
                    iter1++;
                }
                if (iter1 == key.size())
                {
                    isFind = false;
                    j--;
                    continue;
                }
                matrix[i][j] = key[iter1];
                keySet.insert(key[iter1]);
                iter1++;
                if (iter1 == key.size())
                {
                    isFind = false;
                }
            }
            else
            {
                matrix[i][j] = *iter2;
                iter2 = next(iter2);
            }
        }
    }
    vector<pair<char, char>> ptext;
    for (int i = 1; i < text.size(); i += 2)
    {
        if (text[i] == text[i - 1])
        {
            ptext.push_back({text[i - 1], 'x'});
        }
        else
        {
            ptext.push_back({text[i - 1], text[i]});
        }
    }
    if (text.size() & 1)
    {
        ptext.push_back({text.back(), 'x'});
    }
    string encrypted;
    map<char, pair<int, int>> mapCord;
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            mapCord[matrix[i][j]] = {i, j};
        }
    }
    for (int i = 0; i < ptext.size(); i++)
    {
        pair<int, int> cor1 = mapCord[ptext[i].first], cor2 = mapCord[ptext[i].second];
        if (cor1.first == cor2.first)
        {
            encrypted += matrix[cor1.first][(cor1.second + 1) % 5];
            encrypted += matrix[cor2.first][(cor2.second + 1) % 5];
        }
        else if (cor1.second == cor2.second)
        {
            encrypted += matrix[(cor1.first + 1) % 5][cor1.second];
            encrypted += matrix[(cor2.first + 1) % 5][cor2.second];
        }
        else
        {
            encrypted += matrix[cor1.first][cor2.second];
            encrypted += matrix[cor2.first][cor1.second];
        }
    }
    cout << "Encrypted : " << encrypted << "\n";
}

void Decryption()
{
    string text, key;
    UserInput(key, text);
    text = RemoveSpaces(text);
    key = RemoveSpaces(key);
    replaceStringJ(key);
    replaceStringJ(text);
    transform(key.begin(), key.end(), key.begin(), ::tolower);
    transform(text.begin(), text.end(), text.begin(), ::tolower);

    // store the char in mat
    vector<vector<char>> matrix(5, vector<char>(5));

    set<char> keySet, remSet;
    bool isFind = true;
    for (int i = 0; i < 26; i++)
    {
        remSet.insert(i + 'a');
    }
    remSet.erase('j');
    for (auto x : key)
    {
        remSet.erase(x);
    }
    auto iter1 = 0;
    auto iter2 = remSet.begin();

    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            if (isFind)
            {
                while (iter1 < key.size() && keySet.count(key[iter1]))
                {
                    iter1++;
                }
                if (iter1 == key.size())
                {
                    isFind = false;
                    j--;
                    continue;
                }
                matrix[i][j] = key[iter1];
                keySet.insert(key[iter1]);
                iter1++;
                if (iter1 == key.size())
                {
                    isFind = false;
                }
            }
            else
            {
                matrix[i][j] = *iter2;
                iter2 = next(iter2);
            }
        }
    }

    vector<pair<char, char>> ptext;
    for (int i = 1; i < text.size(); i += 2)
    {
        if (text[i] == text[i - 1])
        {
            ptext.push_back({text[i - 1], 'x'});
        }
        else
        {
            ptext.push_back({text[i - 1], text[i]});
        }
    }
    if (text.size() & 1)
    {
        ptext.push_back({text.back(), 'x'});
    }
    string decrypted;
    map<char, pair<int, int>> mapCord;
    for (int i = 0; i < 5; i++)
    {
        for (int j = 0; j < 5; j++)
        {
            mapCord[matrix[i][j]] = {i, j};
        }
    }
    for (int i = 0; i < ptext.size(); i++)
    {
        pair<int, int> cor1 = mapCord[ptext[i].first], cor2 = mapCord[ptext[i].second];
        if (cor1.first == cor2.first)
        {
            decrypted += matrix[cor1.first][((cor1.second - 1) % 5 + 5) % 5];
            decrypted += matrix[cor2.first][((cor2.second - 1) % 5 + 5) % 5];
        }
        else if (cor1.second == cor2.second)
        {
            decrypted += matrix[((cor1.first - 1) % 5 + 5) % 5][cor1.second];
            decrypted += matrix[((cor2.first - 1) % 5 + 5) % 5][cor2.second];
        }
        else
        {
            decrypted += matrix[cor1.first][cor2.second];
            decrypted += matrix[cor2.first][cor1.second];
        }
    }
    cout << "Decrypted : " << decrypted << "\n";
}

int main()
{
    // system("clear");
    int op;
    while (true)
    {
        printLine();
        cout << "____The Encrypt And Decrypt Program____\n";
        cout << "1.Encryption\n";
        cout << "2.Decryption\n";
        cout << "Choose an option...\n";
        printLine();
        cin >> op;
        printLine();
        switch (op)
        {
        case 1:
            Encryption();
            break;
        case 2:
            Decryption();
            break;
        default:
            cout << "Program Terminated Bcoz Of Invalid Input!\n";
            return 0;
        }
        printLine();
    }
    return 0;
}

/*
Edge Cases
1.Handle the corner cases which is adding the suffix correctly
2.
*/