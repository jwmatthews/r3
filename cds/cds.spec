Name:           pulp-v2-cds
Version:        1.0.1
Release:        1%{?dist}
Summary:        A lightweight distribution system for pulp v2 content. 

Group:          Development/Languages
License:        GPLv2
URL:            https://fedorahosted.org/pulp/
Source0:        https://fedorahosted.org/releases/p/u/pulp/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  rpm-python

Requires: mod_wsgi

%description
A lightweight distribution system for pulp v2 content.

%prep
%setup -q 

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp etc/httpd/conf.d/pulp-cds.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/

mkdir -p $RPM_BUILD_ROOT/etc/pulp
cp etc/pulp/repo_auth.conf $RPM_BUILD_ROOT/etc/pulp/

mkdir -p $RPM_BUILD_ROOT/srv/pulp/
cp srv/pulp/repo_auth.wsgi $RPM_BUILD_ROOT/srv/pulp

%clean
rm -rf %{buildroot}

%files
%defattr(-,apache,apache,-)
%{python_sitelib}/pulp/cds/
%{python_sitelib}/pulp/repo_auth/
%attr(775, apache, apache) /srv/pulp
%attr(750, apache, apache) /srv/pulp/repo_auth.wsgi
%config %{_sysconfdir}/httpd/conf.d/pulp-cds.conf
%config(noreplace) %{_sysconfdir}/pulp/repo_auth.conf
%attr(3775, apache, apache) /var/lib/pulp-cds
%attr(3775, apache, apache) /var/log/pulp-cds
