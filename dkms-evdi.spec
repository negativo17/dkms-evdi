%global debug_package %{nil}
%global dkms_name evdi

Name:       dkms-%{dkms_name}
Version:    1.14.11
Release:    2%{?dist}
Summary:    DisplayLink VGA/HDMI display driver kernel module
License:    GPLv2
URL:        https://github.com/DisplayLink/evdi
BuildArch:  noarch

Source0:    %{url}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
Source1:    %{name}.conf
# Required for CentOS Stream (10.1), not required for 10.0:
Patch1:     0001-Revert-CentOS-Stream-10-change.patch

BuildRequires:  sed

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
The DisplaLink %{version} display driver kernel module for kernel %{kversion}.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%prep
%autosetup -p1 -n %{dkms_name}-%{version}
cp %{SOURCE1} module/dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' module/dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr module/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q --force
dkms install -m %{dkms_name} -v %{version} -q --force

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
* Wed Oct 08 2025 Simone Caronni <negativo17@gmail.com> - 1.14.11-2
- Fix modules not getting rebuilt when reinstalling package.
- Do not filter out as success module build steps.

* Tue Sep 02 2025 Simone Caronni <negativo17@gmail.com> - 1.14.11-1
- Update to 1.14.11.

* Thu Jun 19 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-4
- Revert change that works for CentOS Stream (10.1) but not for EL (10.0).

* Wed May 21 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-3
- Add upstream patches.

* Tue May 20 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-2
- Make sure the DKMS configuration is properly overwritten.

* Wed May 14 2025 Simone Caronni <negativo17@gmail.com> - 1.14.10-1
- Update to 1.14.10.

* Fri Mar 28 2025 Simone Caronni <negativo17@gmail.com> - 1.14.9-1
- Update to 1.14.9.

* Sat Feb 08 2025 Simone Caronni <negativo17@gmail.com> - 1.14.8-2
- Simplify DKMS configuration.
- Do not set NO_WEAK_MODULES on Fedora, it does not have kABI support.

* Sun Dec 22 2024 Simone Caronni <negativo17@gmail.com> - 1.14.8-1
- Update to 1.14.8.

* Fri Dec 06 2024 Simone Caronni <negativo17@gmail.com> - 1.14.7-3
- Add kernel 6.12 & EL 9.5 patches.
- Trim changelog.

* Wed Oct 16 2024 Simone Caronni <negativo17@gmail.com> - 1.14.7-2
- Do not uninstall in preun scriptlet in case of an upgrade.

* Sun Sep 29 2024 Simone Caronni <negativo17@gmail.com> - 1.14.7-1
- Update to 1.14.7.

* Thu Aug 15 2024 Simone Caronni <negativo17@gmail.com> - 1.14.6-3
- Update to 1.14.6 final.

* Mon Aug 12 2024 Simone Caronni <negativo17@gmail.com> - 1.14.5-2.20240726giteab561a
- Update to latest snapshot to allow building on kernel 6.10.

* Tue Jul 02 2024 Simone Caronni <negativo17@gmail.com> - 1.14.5-1
- Update to 1.14.5.

* Tue Apr 16 2024 Simone Caronni <negativo17@gmail.com> - 1.14.4-1
- Update to 1.14.4.

* Thu Feb 08 2024 Simone Caronni <negativo17@gmail.com> - 1.14.2-1
- Update to final 1.14.2.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 1.14.1-5.20240130gitd21a6ea
- Update to latest snapshot.

* Mon Jan 08 2024 Simone Caronni <negativo17@gmail.com> - 1.14.1-4.20240104git0313eca
- Update to latest snapshot.
