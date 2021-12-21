# cobra

## install

```bash
linux:~ $ go get -u github.com/spf13/cobra/cobra

linux:~ $ export PATH=$PATH:$(go env GOPATH)/bin
linux:~ $ which cobra
```

---

## hello

### create project

```bash
# create folder
linux:~ $ mkdir hello
linux:~ $ cd hello

# init project
linux:~/hello $ go mod init hello

# create exampl
linux:~/hello $ cobra init .
linux:~/hello $ tree .
```


### build command

```bash
# build binary
linux:~/hello $ go build

# run command
linux:~/hello $ ./hello --help
linux:~/hello $ ./hello
```


### source code

```go
// main.go
package main

import "hello/cmd"

func main() {
	cmd.Execute()
}
```

```go
// cmd/root.go
package cmd

import (
	"os"

	"github.com/spf13/cobra"
)

var rootCmd = &cobra.Command{
	Use:   "hello",
	Short: "A brief description of your application",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
}
```


### flag

```go
// cmd/root.go
package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var name string

var rootCmd = &cobra.Command{
	Use:   "hello",
	Short: "A brief description of your application",
	Long: `A longer description that spans multiple lines and likely contains
examples and usage of using your application. For example:

Cobra is a CLI library for Go that empowers applications.
This application is a tool to generate the needed files
to quickly create a Cobra application.`,
	Run: func(cmd *cobra.Command, args []string) {
		if len(name) == 0 {
			name = "world"
		}
		fmt.Printf("hello %s\n", name)
	},
}

func Execute() {
	err := rootCmd.Execute()
	if err != nil {
		os.Exit(1)
	}
}

func init() {
	rootCmd.Flags().BoolP("toggle", "t", false, "Help message for toggle")
	rootCmd.Flags().StringVarP(&name, "name", "n", "", "name")
}
```


### subcommand

```bash
linux:~/hello $ cobra add demo
linux:~/hello $ cat cmd/demo.go

linux:~/hello $ go build
linux:~/hello $ ./hello -h
linux:~/hello $ ./hello demo
```
