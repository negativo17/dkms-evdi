%global commit0 64559211ec33390dbf4372e1029455ff58e0e739
%global date 20230223
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

%global debug_package %{nil}
%global dkms_name evdi

Name:       dkms-%{dkms_name}
Version:    1.12.0
Release:    3%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
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
Source2:    dkms-no-weak-modules.conf

Patch0:     %{dkms_name}-el.patch

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
* Thu Mar 02 2023 Simone Caronni <negativo17@gmail.com> - 1.12.0-3.20230223git6455921
- Fix build on latest EL 8/9 and Fedora kernels.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 1.12.0-2.20221013gitbdc258b
- Update to latest snapshot.

* Tue Aug 09 2022 Simone Caronni <negativo17@gmail.com> - 1.12.0-1.20220725gitb884877
- Update to latest 1.12.0 snapshot.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 1.11.0-2.20220428git39da217
- Add patch for CentOS/RHEL 8.6.

* Sat Apr 30 2022 Simone Caronni <negativo17@gmail.com> - 1.11.0-1.20220428git39da217
- Update to 1.11.0 snapshot.

* Thu Mar 03 2022 Simone Caronni <negativo17@gmail.com> - 1.10.1-1
- Update to 1.10.1.

* Fri Jan 21 2022 Simone Caronni <negativo17@gmail.com> - 1.10.0-1.20220104gitaef6790
- Update to 1.10.0 plus latest commits.

* Thu Dec 02 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-4.20211202gitd6b2841
- Update to latest snapshot.

* Fri Sep 03 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-3
- Fix typo.

* Thu Sep 02 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-2
- Update with latest upstream patches.

* Tue Apr 13 2021 Simone Caronni <negativo17@gmail.com> - 1.9.1-1
- First build.
