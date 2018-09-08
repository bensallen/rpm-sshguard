Name:		sshguard
Version:	2.2.0
Release:	1
License:	GPLv2+
Summary:	Protect hosts from brute force attacks against ssh
Url:		http://www.sshguard.net
Group:		Productivity/Networking/Security
Source0:	http://downloads.sourceforge.net/project/sshguard/sshguard/%{version}/%{name}-%{version}.tar.gz
Source1:	sshguard.service
Source2:	sshguard.sysconfig
Source3:	sshguard.whitelist
Source4:	sshguard-journalctl
Requires:	iptables
Requires:	openssh
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
Sshguard protects networked hosts from brute force attacks
against ssh servers. It detects such attacks and blocks the
attacker's address with a firewall rule.

%prep
%setup -q

%build
%configure \
  --with-firewall=iptables
make %{_smp_mflags}

%install
%makeinstall
install -d %{buildroot}%{_unitdir}
install -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/sshguard.service
install -d %{buildroot}/%{_sysconfdir}/sysconfig
install -m 0600 %{SOURCE2} %{buildroot}/%{_sysconfdir}/sysconfig/sshguard
install -d %{buildroot}/%{_sysconfdir}/sshguard
install -m 0600 %{SOURCE3} %{buildroot}/%{_sysconfdir}/sshguard/whitelist
install -d %{buildroot}/%_localstatedir/db/sshguard
install -d %{buildroot}/%{_libexecdir}/sshguard
install -m 0755 %{SOURCE4} %{buildroot}/%{_libexecdir}/sshguard/sshguard-journalctl

%post
/usr/bin/systemctl daemon-reload >/dev/null 2>&1
/usr/bin/systemctl enable sshguard >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ] ; then
    /usr/bin/systemctl stop sshguard >/dev/null 2>&1
    /usr/bin/systemctl disable sshguard >/dev/null 2>&1
fi

%postun
if [ "$1" -ge "1" ] ; then
   /usr/bin/systemctl try-restart sshguard >/dev/null 2>&1 || :
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_sbindir}/sshguard
%{_libexecdir}/sshguard/sshguard-journalctl
%{_libexecdir}/sshg-*
%{_unitdir}/sshguard.service
%config %{_sysconfdir}/sysconfig/sshguard
%config %{_sysconfdir}/sshguard/whitelist
%_localstatedir/db/sshguard
%doc CHANGELOG.rst README.rst examples/
%doc %{_mandir}/man8/%{name}*
%doc %{_mandir}/man7/%{name}*

%changelog
* Sat Sep 08 2018 Ron Valente <ronald.valente@gmail.com> 2.2.0-1
- Upgrade to 2.2.0 Release of SSHGuard
- Added CHANGELOG.rst to doc
- Added man7 for sshguard-setup7
- Added sshg-* to libexec
* Wed Apr 20 2016 Ben Allen <bsallen@alcf.anl.gov> 1.6.3-1
- Initial release (v1.6.3)
