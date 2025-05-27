Name:    ea-nodejs22
Vendor:  cPanel, Inc.
Summary: Node.js 22
Version: 22.16.0
# Doing release_prefix this way for Release allows for OBS-proof versioning, See EA-4572 for more details
%define release_prefix 1
Release: %{release_prefix}%{?dist}.cpanel
License: MIT
Group:   Development/Languages
URL:  https://nodejs.org
Source0: https://nodejs.org/dist/v%{version}/node-v%{version}-linux-x64.tar.gz

Provides: ea4-nodejs
Conflicts: ea4-nodejs
# Because old ea-nodejs10 does not have ^^^ and DNF wants to solve ^^^ by downgrading ea-nodejs10
Conflicts: ea-nodejs10

%description
Node.js is a JavaScript runtime built on Chrome's V8 JavaScript engine.

%prep
%setup -qn node-v%{version}-linux-x64

%build

# nodejs now has support for Microsoft Powershell, since that is not relevant
# to any of our deployed systems, I am removing them so they do not
# automatically require powershell, causing a dependency issue

cat > remove_pwsh.pl <<EOF
use strict;
use warnings;

my @files = split (/\n/, \`find . -type f -print\`);

foreach my \$file (@files) {
    my \$first_line = \`head -n 1 \$file\`;
    if (\$first_line =~ m/env\s+pwsh/) {
        print "Removing file \$file\n";
        unlink \$file;
    }
}
EOF

/usr/bin/perl remove_pwsh.pl

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs22
cp -r ./* $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs22

cd $RPM_BUILD_ROOT/opt/cpanel/ea-nodejs22
for file in `find . -type f -print | xargs grep -l '^#![ \t]*/usr/bin/env node'`
do
    echo "Changing Shebang (env) for" $file
    sed -i '1s:^#![ \t]*/usr/bin/env node:#!/opt/cpanel/ea-nodejs22/bin/node:' $file
done

mkdir -p %{buildroot}/etc/cpanel/ea4
echo -n /opt/cpanel/ea-nodejs22/bin/node > %{buildroot}/etc/cpanel/ea4/passenger.nodejs

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
/opt/cpanel/ea-nodejs22
/etc/cpanel/ea4/passenger.nodejs
%attr(0755,root,root) /opt/cpanel/ea-nodejs22/bin/*


%changelog
* Wed May 21 2025 Cory McIntire <cory.mcintire@webpros.com> - 22.16.0-1
- EA-12884: Update ea-nodejs22 from v22.15.1 to v22.16.0

* Wed May 14 2025 Cory McIntire <cory.mcintire@webpros.com> - 22.15.1-1
- EA-12867: Update ea-nodejs22 from v22.15.0 to v22.15.1
    - Improper error handling in async cryptographic operations crashes process (CVE-2025-23166) - (high)
    - Corrupted pointer in node::fs::ReadFileUtf8(const FunctionCallbackInfo<Value>& args) when args[0] is a string. (CVE-2025-23165) - (low)

* Thu Apr 24 2025 Cory McIntire <cory.mcintire@webpros.com> - 22.15.0-1
- EA-12832: Update ea-nodejs22 from v22.14.0 to v22.15.0

* Tue Feb 11 2025 Cory McIntire <cory.mcintire@webpros.com> - 22.14.0-1
- EA-12694: Update ea-nodejs22 from v22.13.1 to v22.14.0

* Tue Jan 21 2025 Cory McIntire <cory@cpanel.net> - 22.13.1-1
- EA-12664: Update ea-nodejs22 from v22.13.0 to v22.13.1
	- Worker permission bypass via InternalWorker leak in diagnostics (CVE-2025-23083) - (high)
	- GOAWAY HTTP/2 frames cause memory leak outside heap (CVE-2025-23085) - (medium)
	- Path traversal by drive name in Windows environment (CVE-2025-23084) - (medium)

* Tue Jan 07 2025 Cory McIntire <cory@cpanel.net> - 22.13.0-1
- EA-12635: Update ea-nodejs22 from v22.12.0 to v22.13.0

* Tue Dec 03 2024 Cory McIntire <cory@cpanel.net> - 22.12.0-1
- EA-12599: Update ea-nodejs22 from v22.11.0 to v22.12.0

* Mon Nov 04 2024 Cory McIntire <cory@cpanel.net> - 22.11.0-1
- EA-12513: Update ea-nodejs22 from v22.10.0 to v22.11.0

* Wed Oct 16 2024 Cory McIntire <cory@cpanel.net> - 22.10.0-1
- EA-12472: Update ea-nodejs22 from v22.9.0 to v22.10.0

* Tue Sep 17 2024 Cory McIntire <cory@cpanel.net> - 22.9.0-1
- EA-12393: Update ea-nodejs22 from v22.8.0 to v22.9.0

* Tue Sep 03 2024 Cory McIntire <cory@cpanel.net> - 22.8.0-1
- EA-12366: Update ea-nodejs22 from v22.7.0 to v22.8.0

* Thu Aug 22 2024 Cory McIntire <cory@cpanel.net> - 22.7.0-1
- EA-12349: Update ea-nodejs22 from v22.6.0 to v22.7.0

* Tue Aug 06 2024 Cory McIntire <cory@cpanel.net> - 22.6.0-1
- EA-12324: Update ea-nodejs22 from v22.5.0 to v22.6.0

* Thu Jul 18 2024 Cory McIntire <cory@cpanel.net> - 22.5.0-1
- EA-12289: Update ea-nodejs22 from v22.4.1 to v22.5.0

* Tue Jul 09 2024 Cory McIntire <cory@cpanel.net> - 22.4.1-1
- EA-12265: Update ea-nodejs22 from v22.3.0 to v22.4.1
	- CVE-2024-36138 - Bypass incomplete fix of CVE-2024-27980 (High)
	- CVE-2024-22020 - Bypass network import restriction via data URL (Medium)
	- CVE-2024-22018 - fs.lstat bypasses permission model (Low)
 	- CVE-2024-36137 - fs.fchown/fchmod bypasses permission model (Low)
	- CVE-2024-37372 - Permission model improperly processes UNC paths (Low)

* Mon Jul 01 2024 Cory McIntire <cory@cpanel.net> - 22.3.0-1
- EA-12241: Update ea-nodejs22 from v22.2.0 to v22.3.0

* Wed May 15 2024 Cory McIntire <cory@cpanel.net> - 22.2.0-1
- EA-12158: Update ea-nodejs22 from v22.1.0 to v22.2.0

* Mon May 06 2024 Brian Mendoza <brian.mendoza@cpanel.net> - 22.1.0-1
- ZC-11803: Initial build
