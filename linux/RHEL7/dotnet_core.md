# .NET Core

## Install

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

## Hello World

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

centos:~/myApp # dotnet run
centos:~/myApp # dotnet build linux-x64         # define in /usr/share/dotnet/sdk/NuGetFallbackFolder/microsoft.netcore.platforms/2.0.1/runtime.json
centos:~/myApp # ./bin/Debug/netcoreapp2.0/linux-x64/myApp
```

---

## IDE

[Visual Studio Code](https://code.visualstudio.com/)

[Rider](https://www.jetbrains.com/rider/)


---

## Reference

[.NET Core 指南](https://docs.microsoft.com/zh-tw/dotnet/core/)

[.NET Doc](https://docs.microsoft.com/en-us/dotnet/welcome)

[Getting Started Guide For RHEL](https://access.redhat.com/documentation/en-us/net_core/2.0/html/getting_started_guide/)