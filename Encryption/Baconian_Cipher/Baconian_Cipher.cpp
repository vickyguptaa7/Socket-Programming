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

void UserInput(string &text)
{
    cout << "Enter The Text : \n";
    fflush(stdin);
    getline(cin, text);
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
    UserInput(text);
    string newText = RemoveSpaces(text);
    printLine();

    if (isSpecialChars(newText))
    {
        cout << "Founded Special Characters! \nTry Again Without Special Characters!\n";
        return;
    }

    lowerCase(newText);

    int textLen = newText.size();
    int inputLen = textLen * 5;
    string str;
    cout << "The Input String Length Must Be Greater Than " << inputLen << "\n";
    while (true)
    {
        fflush(stdin);
        getline(cin, str);
        str = RemoveSpaces(str);
        if (isSpecialChars(str))
        {
            cout << "Founded Special Characters! \nTry Again Without Special Characters!\n";
            continue;
        }
        printLine();
        if (str.size() >= inputLen)
        {
            break;
        }
        cout << "The Input String Length Must Be Greater Than " << inputLen << "!\nTry Again!\n";
    }
    lowerCase(str);
    string halfEncrypt;
    for (auto ch : newText)
    {
        int num = ch - 'a';
        int iter = 0;
        while (iter < 5)
        {
            halfEncrypt += (num & 1) ? 'b' : 'a';
            num /= 2;
            iter++;
        }
    }
    string encrypt;
    for (int i = 0; i < halfEncrypt.size(); i++)
    {
        if (halfEncrypt[i] == 'a')
            encrypt += str[i];
        else
            encrypt += char(str[i] - 32);
    }
    cout << "The Encrypted String : \n";
    cout << encrypt << "\n";
    cout << "String Encrypted Successfully\n";
    printLine();
}

void Decryption()
{
    string text;
    UserInput(text);
    string newText = RemoveSpaces(text);
    int textLen = newText.size();
    string btext;
    printLine();
    if (isSpecialChars(newText))
    {
        cout << "Founded Special Characters! \nTry Again Without Special Characters!\n";
        return;
    }

    for (int i = 0; i < text.size(); i++)
    {
        if (newText[i] >= 'a' && newText[i] <= 'z')
        {
            btext += "0";
        }
        else
        {
            btext += "1";
        }
    }
    if (btext.size() % 5 != 0)
    {
        cout << "Your Encrypted Key Is Corrupted!\nTry Again!\n";
        return;
    }
    string decrypt;
    for (int i = 0; i < btext.size(); i += 5)
    {
        int deci = 0;
        for (int j = 4; j >= 0; j--)
        {
            if (btext[i + j] == '1')
            {
                deci += (1 << (j));
            }
        }
        decrypt += char(deci + 'a');
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