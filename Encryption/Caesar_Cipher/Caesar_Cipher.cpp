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

void UserInput(string &text, int &shift)
{
    cout << "Enter The Text : \n";
    fflush(stdin);
    getline(cin, text);
    cout << "Enter The Shift : \n";
    cin >> shift;
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

void lowerCase(string &text)
{
    for (int i = 0; i < text.size(); i++)
    {
        if (text[i] >= 'A' && text[i] <= 'Z')
        {
            text[i] += 32;
        }
    }
}

bool isSpecialChars(string text)
{
    for (auto ch : text)
    {
        if (ch >= 'a' && ch <= 'z')
            continue;
        if (ch >= 'A' && ch <= 'Z')
            continue;
        return true;
    }
    return false;
}

void Encryption()
{
    string text;
    int shift;
    UserInput(text, shift);
    text = RemoveSpaces(text);
    printLine();

    if (isSpecialChars(text))
    {
        cout << "Founded Special Characters! \nTry Again Without Special Characters!\n";
        return;
    }

    lowerCase(text);

    int textLen = text.size();
    string encrypt;
    for (int i = 0; i < textLen; i++)
    {
        encrypt += (text[i] - 'a' + shift) % 26 + 'a';
    }
    cout << "The Encrypted String : \n";
    cout << encrypt << "\n";
    cout << "String Encrypted Successfully\n";
    printLine();
}

void Decryption()
{
    string text;
    int shift;
    UserInput(text, shift);
    text = RemoveSpaces(text);
    int textLen = text.size();

    if (isSpecialChars(text))
    {
        cout << "Founded Special Characters! \nTry Again Without Special Characters!\n";
        return;
    }
    string decrypt;
    for (int i = 0; i < textLen; i++)
    {
        decrypt += ((text[i] - 'a' - shift) % 26 + 26) % 26 + 'a';
    }
    cout << "The Decrypted String : \n";
    cout << decrypt << "\n";
    cout << "String Decrypted Successfully!\n";
    printLine();
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