Name:		shadowsocks-libev
Version:	3.1.0
Release:	1%{?dist}
Summary:	A lightweight and secure socks5 proxy

Group:		Applications/Internet
License:	GPLv3+
URL:		https://github.com/madeye/%{name}
Source0:	%{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:	libsodium-devel >= 1.0.4
BuildRequires:	mbedtls-devel
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	gawk
BuildRequires:	asciidoc
BuildRequires:	xmlto
BuildRequires:	gettext
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	automake
BuildRequires:	make
BuildRequires:	zlib-devel
BuildRequires:	c-ares-devel
BuildRequires:	libev-devel
Requires:   libsodium >= 1.0.4
Requires:   mbedtls
Requires:	pcre
Requires:	zlib
Requires:	c-ares
Requires:	libev

%if 0%{?rhel} != 6
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: systemd
%endif

Conflicts:	python-shadowsocks python3-shadowsocks

AutoReq:	no

%description
shadowsocks-libev is a lightweight secured socks5 proxy for embedded devices and low end boxes.


%prep
%setup -q


%build
%configure --enable-shared
make clean
%make_build


%install
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/etc/shadowsocks-libev
%if 0%{?rhel} == 6
mkdir -p %{buildroot}%{_initddir}
install -m 755 %{_builddir}/%{buildsubdir}/rpm/SOURCES/etc/init.d/shadowsocks-libev %{buildroot}%{_initddir}/shadowsocks-libev
%else
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{_builddir}/%{buildsubdir}/rpm/SOURCES/systemd/shadowsocks-libev.default %{buildroot}%{_sysconfdir}/sysconfig/shadowsocks-libev
install -m 644 %{_builddir}/%{buildsubdir}/rpm/SOURCES/systemd/shadowsocks-libev*.service %{buildroot}%{_unitdir}/
%endif
install -m 644 %{_builddir}/%{buildsubdir}/debian/config.json %{buildroot}%{_sysconfdir}/shadowsocks-libev/config.json


%post
%if 0%{?rhel} == 6
/sbin/chkconfig --add shadowsocks-libev
%else
%systemd_post shadowsocks-libev.service
%endif

%preun
%if 0%{?rhel} == 6
if [ $1 -eq 0 ]; then
    /sbin/service shadowsocks-libev stop
    /sbin/chkconfig --del shadowsocks-libev
fi
%else
%systemd_preun shadowsocks-libev.service
%endif

%if 0%{?rhel} != 6
%postun
%systemd_postun_with_restart shadowsocks-libev.service
%endif


%files
%{_bindir}/*
%{_libdir}/*
%config(noreplace) %{_sysconfdir}/shadowsocks-libev/config.json
%doc %{_mandir}/*
%doc %{_defaultdocdir}/shadowsocks-libev
%if 0%{?rhel} == 6
%{_initddir}/shadowsocks-libev
%else
%{_unitdir}/shadowsocks-libev*.service
%config(noreplace) %{_sysconfdir}/sysconfig/shadowsocks-libev
%endif

%package devel
Summary:    Development files for shadowsocks-libev
License:    GPLv3+

%description devel
Development files for shadowsocks-libev

%files devel
%{_includedir}/*

%changelog

