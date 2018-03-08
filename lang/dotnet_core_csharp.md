# .NET Core - C# #

## 使用環境

### 安裝

```bash
centos:~ # rpm --import https://packages.microsoft.com/keys/microsoft.asc
centos:~ # vi /etc/yum.repos.d/dotnetdev.repo
[packages-microsoft-com-prod]
name=packages-microsoft-com-prod
baseurl= https://packages.microsoft.com/yumrepos/microsoft-rhel7.3-prod
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc

centos:~ # yum install libunwind libicu
centos:~ # yum install dotnet-sdk-2.1.4
centos:~ # dotnet --version

centos:~ # dotnet -h
centos:~ # dotnet new -h
```

---

### Hello World

```bash
centos:~ # dotnet new console -o myApp
centos:~ # cd myApp
centos:~/myApp # cat Program.cs
using System;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
        }
    }
}

# 直接執行方式 
centos:~/myApp # dotnet run

# 先編譯 binary
centos:~/myApp # dotnet build linux-x64         # define in /usr/share/dotnet/sdk/NuGetFallbackFolder/microsoft.netcore.platforms/2.0.1/runtime.json
# 再執行 binary 
centos:~/myApp # ./bin/Debug/netcoreapp2.0/linux-x64/myApp
```

---

### IDE

[Visual Studio Code](https://code.visualstudio.com/)

[Rider](https://www.jetbrains.com/rider/)


---

## 資料型態

### 字串/String

```cs
string name = "C#";
string message = "Hello " + name;
Console.WriteLine(message);
Console.WriteLine($"Hi {name}");

Console.WriteLine("Len: " + name.Length);
Console.WriteLine($"Len: {name.Length}");

Console.WriteLine(message.ToUpper());
Console.WriteLine(message.ToLower());

Console.WriteLine(message.Replace("Hello", "Hi"));
Console.WriteLine(message.Contains("Hello"));
```

---

### 數值/Number

`int`

```cs
int a = 7;
int b = 4;
int c = 3;
int d = a + b * c;
int e = (a + b) / c;
int f = (a + b) % c;

int max = int.MaxValue;
int min = int.MinValue;
```

`double`

```cs
double a = 5;
double b = 4;
double c = 2;
double d = (a  + b) / c;

double max = double.MaxValue;
double min = double.MinValue;
```

`decimal`

```cs
decimal min = decimal.MinValue;
decimal max = decimal.MaxValue;

double a = 1.0;
double b = 3.0;

decimal c = 1.0M;
decimal d = 3.0M;
```

### 集合/Collection

`array`

```cs
string[] weekDays = { "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" };

for (int i = 0; i < weekDays.Length; i++) {Console.WriteLine(weekDays[i]);}
foreach (string day in weekDays) {Console.WriteLine(day);}

int[,] array2D = new int[,] { { 1, 2 }, { 3, 4 }, { 5, 6 }, { 7, 8 } };
for (int i = 0; i < array2D.GetLength(0); i++)
{
    for (int j = 0; j < array2D.GetLength(1); j++) {Console.WriteLine(array2D[i, j]);}
}
foreach (int i in array2D) {Console.WriteLine(i);}

```

`list`

```cs
using System;
using System.Collections.Generic;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            List<string> students = new List<string>();
            students.Add("John");
            students.Add("Mary");

            foreach (string student in students) {Console.WriteLine(student);}
            Console.WriteLine(String.Join(",", students.ToArray()));

            students.AddAt(0);
            students.Add("Mary");
        }
    }
}

```

`dictionary`

```cs
using System;
using System.Collections.Generic;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Dictionary<string, string> openWith = new Dictionary<string, string>();
            openWith.Add("txt", "notepad.exe");
            openWith.Add("bmp", "paint.exe");
            
            foreach (var item in openWith) {Console.WriteLine("key: " + item.Key + ", value: " + item.Value);}
        }
    }
}
```


---

## 控制流程

### if/else

```cs
using System;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Write("input your sex [m/f]: ");
            string sex = Console.ReadLine();
            if (sex == "m")
            {
                Console.WriteLine("Male");
            }
            else if (sex == "f")
            {
                Console.WriteLine("Female");
            }
            else {
                Console.WriteLine("Unknown");
            }
        }
    }
}
```

```cs
using System;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            var os = Environment.OSVersion;
            string p;

            if (os.Platform.ToString() == "Unix")
                p = "Unix-Like";
            else
                p = "Unknown";
            Console.WriteLine(p1);

            // 另一種簡單的 if/else 方式
            string p2 = (os.Platform.ToString() == "Unix") ? "Unix-Like" : "Unknown";
            Console.WriteLine(p2);
        }
    }
}
```

```cs
using System;
using System.IO;

namespace myApp
{
    class Program
    {
        static void Main(string[] args)
        {
            string filePath1 = Path.Combine(Environment.GetEnvironmentVariable("HOME"), ".bashrc");
            string filePath2 = Path.Combine(Environment.GetEnvironmentVariable("HOME"), ".profile");
            Console.WriteLine(File.Exists(filePath1) || File.Exists(filePath2) ? ".profile or .bashrc exist" : "File does not exist.");
        }
    }
}
```

---

### for


---

## Reference

[.NET Core 指南](https://docs.microsoft.com/zh-tw/dotnet/core/)

[.NET Doc](https://docs.microsoft.com/en-us/dotnet/welcome)

[Getting Started Guide For RHEL](https://access.redhat.com/documentation/en-us/net_core/2.0/html/getting_started_guide/)

[C# 快速入門](https://docs.microsoft.com/zh-tw/dotnet/csharp/quick-starts/index)

[C# Quickstarts](https://docs.microsoft.com/en-us/dotnet/csharp/quick-starts/index)