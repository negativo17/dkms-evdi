%global commit0 eab561a9fe19d1bbc801dd1ec60e8b3318941be7
%global date 20240726
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

%global debug_package %{nil}
%global dkms_name evdi

Name:       dkms-%{dkms_name}
Version:    1.14.9%{!?tag:^%{date}git%{shortcommit0}}
Release:    1%{?dist}
Summary:    DisplayLink VGA/HDMI display driver kernel module
License:    GPLv2
URL:        https://github.com/DisplayLink/evdi
BuildArch:  noarch

%if 0%{?tag:1}
Source0:    %{url}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
%else
Source0:    %{url}/archive/%{commit0}.tar.gz#/%{dkms_name}-%{shortcommit0}.tar.gz
%endif
Source1:    %{name}.conf

BuildRequires:  sed

Provides:   %{dkms_name}-kmod = %{?epoch:%{epoch}:}%{version}
Requires:   %{dkms_name}-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:   dkms

%description
The DisplaLink %{version} display driver kernel module for kernel %{kversion}.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%prep
%if 0%{?tag:1}
%autosetup -p1 -n %{dkms_name}-%{version}
%else
%autosetup -p1 -n %{dkms_name}-%{commit0}
%endif

sed -i -e 's/__VERSION_STRING/%{version}/g' module/dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr module/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%post
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}

%changelog
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
