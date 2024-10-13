# grubby

## install

```bash
alma:~ # dnf install grubby -y
```

---

## usage

```bash
# list default
alma:~ # grubby --default-kernel
alma:~ # grubby --default-index
alma:~ # grubby --default-title

# list all kernel
alma:~ # grubby --info ALL
alma:~ # grubby --info <kernel-path>

# setting default kernel
alma:~ # grubby --set-default <kernel-path>
alma:~ # grubby --set-default-index <entry-index>

# kernel argument
alma:~ # grubby --update-kernel ALL --args selinux=0            # add argument
alma:~ # grubby --update-kernel ALL --remove-args selinux       # remove argument
alma:~ # cat /etc/default/grub                                  # update /etc/default/grub
```
