# sle 16

## cockpit

```bash
sle:~ # zypper in -t pattern cockpit

sle:~ # systemctl status cockpit
sle:~ # systemctl enable cockpit
sle:~ # systemctl start  cockpit

sle:~ # curl http://localhost:9090
```

---

##  scheduling system

### munge

- [munge](https://dun.github.io/munge/)

```bash
sle:~ # zypper in -t pattern devel_basis
sle:~ # zypper in rpm-build
sle:~ # zypper in libbz2-devel libopenssl-devel
```

```bash
sle:~ # curl -LO https://github.com/dun/munge/releases/download/munge-0.5.17/munge-0.5.17.tar.xz
sle:~ # mv munge-0.5.17.tar.xz /usr/src/packages/SOURCES/
sle:~ # vi munge.spec
sle:~ # rpmbuild -ba munge.spec

sle:~ # ls /usr/src/packages/RPMS/x86_64/munge*
sle:~ # rpm -ivh /usr/src/packages/RPMS/x86_64/munge-0.5.17-1.x86_64.rpm /usr/src/packages/RPMS/x86_64/munge-libs-0.5.17-1.x86_64.rpm

sle:~ # systemctl enable munge --now

# Test the daemon
sle:~ # munge -n | unmunge
```

```spec
# munge.spec
Name:           munge
Version:        0.5.17
Release:        1
Summary:        MUNGE authentication service
License:        GPL-3.0-or-later
URL:            https://github.com/dun/munge
Source0:        https://github.com/dun/munge/releases/download/%{name}-%{version}/%{name}-%{version}.tar.xz

# SLES 16 Build Dependencies
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  libbz2-devel
BuildRequires:  libopenssl-devel
BuildRequires:  zlib-devel
BuildRequires:  pkg-config
BuildRequires:  systemd-rpm-macros

# User/Group metadata fixes
Requires(pre):  shadow
Provides:       user(munge)
Provides:       group(munge)

# Runtime Dependencies
Requires:       %{name}-libs = %{version}-%{release}
Requires:       logrotate
%{?systemd_requires}

%description
MUNGE (MUNGE Uid 'N' Gid Emporium) is an authentication service for creating
and validating user credentials.

%package devel
Summary:        Development files for the MUNGE authentication service
Requires:       %{name}-libs = %{version}-%{release}

%description devel
Header files and libraries for developing applications that use MUNGE.

%package libs
Summary:        Shared library for the MUNGE authentication service

%description libs
The shared library (libmunge) required to run applications using MUNGE.

%prep
%setup -q

%build
%configure --disable-static \
    --with-crypto-lib=openssl \
    --with-logrotateddir=%{_sysconfdir}/logrotate.d \
    --with-pkgconfigdir=%{_libdir}/pkgconfig \
    --with-runstatedir=%{_rundir} \
    --with-systemdsysusersdir=%{_sysusersdir} \
    --with-systemdunitdir=%{_unitdir}
%make_build

%install
%make_install
rm -f %{buildroot}%{_libdir}/libmunge.la

# Setup directory structure and ghost files
mkdir -p %{buildroot}%{_rundir}/munge
touch %{buildroot}%{_rundir}/munge/munged.pid
touch %{buildroot}%{_localstatedir}/lib/munge/munged.seed
touch %{buildroot}%{_localstatedir}/log/munge/munged.log

# Ensure the config dir exists and create a ghost key file
mkdir -p %{buildroot}%{_sysconfdir}/munge
touch %{buildroot}%{_sysconfdir}/munge/munge.key

%pre
getent group munge >/dev/null || groupadd -r munge
getent passwd munge >/dev/null || \
    useradd -r -g munge -d %{_localstatedir}/lib/munge -s /sbin/nologin \
    -c "MUNGE authentication service" munge
exit 0

%post
%service_add_post munge.service

# --- FIX: Auto-generate key if missing ---
if [ ! -s %{_sysconfdir}/munge/munge.key ]; then
    echo "Generating MUNGE cryptographic key..."
    # Use /dev/urandom to create a 1024-byte key if mungekey isn't used
    dd if=/dev/urandom bs=1 count=1024 of=%{_sysconfdir}/munge/munge.key 2>/dev/null
    chown munge:munge %{_sysconfdir}/munge/munge.key
    chmod 0600 %{_sysconfdir}/munge/munge.key
fi

%preun
%service_del_preun munge.service

%postun
%service_del_postun munge.service

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%license COPYING
%doc AUTHORS NEWS README
%dir %attr(0700,munge,munge) %{_sysconfdir}/munge
%attr(0600,munge,munge) %config(noreplace) %ghost %{_sysconfdir}/munge/munge.key
%config(noreplace) %{_sysconfdir}/logrotate.d/munge
%config(noreplace) %{_sysconfdir}/sysconfig/munge
%dir %attr(0700,munge,munge) %{_localstatedir}/lib/munge
%attr(0600,munge,munge) %ghost %{_localstatedir}/lib/munge/munged.seed
%dir %attr(0700,munge,munge) %{_localstatedir}/log/munge
%attr(0640,munge,munge) %ghost %{_localstatedir}/log/munge/munged.log
%dir %attr(0755,munge,munge) %ghost %{_rundir}/munge
%attr(0644,munge,munge) %ghost %{_rundir}/munge/munged.pid
%{_bindir}/munge
%{_bindir}/remunge
%{_bindir}/unmunge
%{_sbindir}/munged
%{_sbindir}/mungekey
%{_mandir}/man1/*
%{_mandir}/man7/*
%{_mandir}/man8/*
%{_unitdir}/munge.service
%{_sysusersdir}/munge.conf

%files devel
%{_includedir}/munge.h
%{_libdir}/libmunge.so
%{_libdir}/pkgconfig/munge.pc
%{_mandir}/man3/*

%files libs
%{_libdir}/libmunge.so.2*
```

### slurm

- [slurm](https://www.schedmd.com/)

```bash
sle:~ # zypper in -t pattern devel_basis
sle:~ # zypper in rpm-build
sle:~ # zypper in libmariadb-devel readline-devel
sle:~ # rpm -ivh /usr/src/packages/RPMS/x86_64/munge-devel-0.5.17-1.x86_64.rpm
```

```bash
sle:~ # curl -LO https://download.schedmd.com/slurm/slurm-25.11.1.tar.bz2
sle:~ # rpmbuild -ta slurm-25.11.1.tar.bz2
sle:~ # ls /usr/src/packages/RPMS/x86_64/slurm*
```
