# condition

## if

```bash
if [ "x$SEX" == "xmale" ]; then
  echo "Hi male"
else
  echo "Hi Female"
fi

[ "x$SEX" == "xmale" ] && echo "Hi male" || echo "Hi Female"
test "x$SEX" == "xmale" && echo "Hi male" || echo "Hi Female"
```


---

## case

```bash
case $SHELL in
  "/bin/bash")
    echo "BASH"
    ;;

  "/bin/tcsh")
    echo "TCSH"
    ;;

  "/bin/zsh")
    echo "ZSH"
    ;;

  *)
    echo "UNKNOWN"
    ;;
esac
```
