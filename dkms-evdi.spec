%global commit0 eab561a9fe19d1bbc801dd1ec60e8b3318941be7
%global date 20240726
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global tag %{version}

%global debug_package %{nil}
%global dkms_name evdi

Name:       dkms-%{dkms_name}
Version:    1.14.7%{!?tag:^%{date}git%{shortcommit0}}
Release:    2%{?dist}
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
dkms add -m %{dkms_name} -v %{version} -q --rpm_safe_upgrade || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
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

* Mon Nov 27 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-3.20231123gita943d98
- Switch to snapshot which include build fixes for latest kernels.

* Mon Nov 20 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-2
- Add patch for 6.6 kernel.

* Wed Aug 23 2023 Simone Caronni <negativo17@gmail.com> - 1.14.1-1
- Update to 1.14.1.

* Fri Jun 02 2023 Simone Caronni <negativo17@gmail.com> - 1.14.0-1
- Update to 1.14.0.

* Wed May 10 2023 Simone Caronni <negativo17@gmail.com> - 1.13.1-2
- Update EL patch.

* Wed Mar 29 2023 Simone Caronni <negativo17@gmail.com> - 1.13.1-1
- Update to 1.13.1.

* Fri Mar 17 2023 Simone Caronni <negativo17@gmail.com> - 1.13.0-1
- Update to 1.13.0.

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
