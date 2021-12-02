%global commit0 d6b28414a4ceb41a904077318b48fa8a7d8981d1
%global date 20211202
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global debug_package %{nil}
%global dkms_name evdi

Name:       dkms-%{dkms_name}
Version:    1.9.1
Release:    4%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:    DisplayLink VGA/HDMI display driver kernel module
License:    GPLv2
URL:        https://github.com/DisplayLink/evdi
BuildArch:  noarch

%if 0%{?tag:1}
Source0:    https://github.com/DisplayLink/%{dkms_name}/archive/v%{version}.tar.gz#/%{dkms_name}-%{version}.tar.gz
%else
Source0:    https://github.com/DisplayLink/%{dkms_name}/archive/%{commit0}.tar.gz#/%{dkms_name}-%{shortcommit0}.tar.gz
%endif
Source1:    %{name}.conf
Source2:    dkms-no-weak-modules.conf

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

cp -f %{SOURCE1} module/dkms.conf

sed -i -e 's/__VERSION_STRING/%{version}/g' module/dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr module/* %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
* Thu Dec 02 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-4.20211202gitd6b2841
- Update to latest snapshot.

* Fri Sep 03 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-3
- Fix typo.

* Thu Sep 02 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-2
- Update with latest upstream patches.

* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-1
- First build.
