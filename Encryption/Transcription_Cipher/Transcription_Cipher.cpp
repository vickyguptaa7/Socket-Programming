#include <iostream>
#include <math.h>
#include <vector>
#include <algorithm>
using namespace std;

void printLine()
{
    for (int i = 0; i < 100; i++)
    {
        cout << "-";
    }
    cout << "\n";
}

void UserInput(int &key, string &text)
{
    cout << "Enter The Key : \n";
    cin >> key;
    cout << "Enter The Text : \n";
    fflush(stdin);
    getline(cin, text);
    printLine();
}

int PatternMatching(string text)
{
    string pattern = "Vabcd";
    int indx = -1, textLen = text.size(), patLen = pattern.size();
    for (int i = 0; i <= textLen - patLen; i++)
    {
        bool isTrue = true;
        for (int j = 0; j < patLen; j++)
        {
            if (text[i + j] != pattern[j])
            {
                isTrue = false;
                break;
            }
        }
        if (isTrue)
        {
            indx = i;
            break;
        }
    }
    return indx;
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

void Encryption()
{
    int key;
    string text;
    UserInput(key, text);
    string newText = RemoveSpaces(text);

    // store the char in mat
    vector<vector<char>> matrix;

    int textLen = newText.size();

    // least required rows
    int rows = ceil(textLen / (double)key);

    // iterator for the new newText
    int textIndx = 0;

    // to store the suffix in the matrix
    char alpha = 'a';

    // used to know when to start adding the suffix
    bool addSuffix = false;

    for (int i = 0; i < rows; i++)
    {
        vector<char> row;
        for (int j = 0; j < key; j++)
        {
            if (textIndx < textLen)
            {
                // adding the user input chars
                row.push_back(newText[textIndx++]);
            }
            else
            {
                // adding the suffix to indicate the termination
                if (addSuffix == false)
                {
                    addSuffix = true;
                    row.push_back('V');
                }
                else
                {
                    row.push_back(alpha);
                    if (alpha != 'e')
                    {
                        alpha++;
                    }
                }
            }
        }
        matrix.push_back(row);
    }

    // if the suffix is not been completed full so we add the remaining suffix
    if (alpha != 'e')
    {
        bool reached = false;
        for (int j = 0; j < 6; j++)
        {
            vector<char> row;
            for (int i = 0; i < key; i++)
            {
                if (addSuffix == false)
                {
                    row.push_back('V');
                    addSuffix = true;
                }
                else
                {
                    row.push_back(alpha);
                    if (alpha != 'e')
                    {
                        alpha++;
                    }
                    else
                    {
                        reached = true;
                    }
                }
            }
            matrix.push_back(row);
            if (reached)
                break;
        }
    }

    // the encrypted text
    string encrypted;
    for (int i = 0; i < matrix[0].size(); i++)
    {
        for (int j = 0; j < matrix.size(); j++)
        {
            encrypted += matrix[j][i];
        }
    }
    printLine();
    cout << "The Encrypted Text : \n";
    cout << encrypted << "\n";
    printLine();
}

void Decryption()
{
    int key;
    string text;
    UserInput(key, text);
    string newText = RemoveSpaces(text);

    int textLen = newText.size();
    int rows = textLen / key, cols = key;

    if ((textLen % key) != 0 || (rows * cols) != textLen)
    {
        cout << "The Input Encryption Is Corrputed!\n";
        cout << "Decryption Exited!\n";
        return;
    }

    vector<vector<char>> matrix(rows, vector<char>(cols));
    int textIndx = 0;
    for (int i = 0; i < cols; i++)
    {
        for (int j = 0; j < rows; j++)
        {
            matrix[j][i] = newText[textIndx++];
        }
    }
    
    string res;
    for (auto x : matrix)
    {
        for (auto y : x)
        {
            res += y;
        }
    }

    string decrypted;
    if (PatternMatching(res) != -1)
    {
        int indx = PatternMatching(res);
        decrypted = res.substr(0, indx);
    }
    else
    {
        cout << "The Input Encryption Is Corrputed!\n";
        cout << "Decryption Exited!\n";
        return;
    }
    cout << "The Decrypted Text : \n";
    cout << decrypted << "\n";
}

int main()
{
    system("clear");
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