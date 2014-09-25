Name:           pulp-v2-cds
Version:        1.0.4
Release:        1%{?dist}
Summary:        A lightweight distribution system for pulp v2 content. 

Group:          Development/Languages
License:        GPLv2
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  rpm-python
BuildRequires:  python-setuptools

Requires:       python >= 2.6
Requires:       mod_wsgi
Requires:       mod_ssl
Conflicts:      pulp-v2-cds-server

%description
A lightweight distribution system for pulp v2 content.

%prep
%setup -q -n rh-rhui-tools-%{version}

%build
pushd src
%{__python} setup.py build
popd

%install
rm -rf $RPM_BUILD_ROOT

# Python setup
pushd src
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
popd
rm -f $RPM_BUILD_ROOT%{python_sitelib}/rhui*egg-info/requires.txt

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
cp etc/httpd/conf.d/pulp-cds.conf $RPM_BUILD_ROOT/etc/httpd/conf.d/

mkdir -p $RPM_BUILD_ROOT/etc/pulp
cp etc/pulp/repo_auth.conf $RPM_BUILD_ROOT/etc/pulp/

mkdir -p $RPM_BUILD_ROOT/srv/pulp/
cp srv/pulp/* $RPM_BUILD_ROOT/srv/pulp

#mkdir -p $RPM_BUILD_ROOT/%{python_sitelib}/pulp/
#cp -r src/* $RPM_BUILD_ROOT/%{python_sitelib}/pulp/

mkdir -p $RPM_BUILD_ROOT/usr/sbin/
cp scripts/* $RPM_BUILD_ROOT/usr/sbin/

mkdir -p $RPM_BUILD_ROOT/etc/pki/pulp/content

mkdir -p $RPM_BUILD_ROOT/var/lib/pulp
mkdir -p $RPM_BUILD_ROOT/var/log/pulp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,apache,apache,-)
%{python_sitelib}/pulp_cds/
%attr(3775, root, root) /usr/sbin/generate_client_certs.py
%attr(775, apache, apache) /srv/pulp
%config %{_sysconfdir}/httpd/conf.d/pulp-cds.conf
%config(noreplace) %{_sysconfdir}/pulp/repo_auth.conf
%attr(3775, root, root) %{_sysconfdir}/pki/pulp/
%attr(3775, apache, apache) /var/lib/pulp
%attr(3775, apache, apache) /var/log/pulp

%post
touch /var/lib/pulp/.cluster-members
touch /var/lib/pulp/.cluster-members-lock

chown apache:apache /var/lib/pulp/.cluster-members-lock
chown apache:apache /var/lib/pulp/.cluster-members

semanage fcontext -a -t httpd_user_rw_content_t '/var/lib/pulp(/.*)?'
semanage fcontext -a -t httpd_user_rw_content_t '/srv/pulp(/.*)?'
restorecon -Rv /var/lib/pulp/*
restorecon -Rv /srv/pulp/*

%postun
if [ $1 -eq 0] ; then # final removal
semanage fcontext -d -t httpd_user_rw_content_t '/var/lib/pulp(/.*)?'
semanage fcontext -d -t httpd_user_rw_content_t '/srv/pulp(/.*)?'
fi

%changelog
* Thu Aug 07 2014 David Gao <jinmaster923@gmail.com> 1.0.4-1
- Added conflict rules. Clean up %%post selinux rule. (jinmaster923@gmail.com)
- Moved appropriate configuration over to cds_api. (jinmaster923@gmail.com)
- Renaming rhui_cds to src folder. Moved cds_api to srv/pulp/
  (jinmaster923@gmail.com)
- Moved source code to their respective component folder.
  (jinmaster923@gmail.com)

* Tue Jul 29 2014 David Gao <jinmaster923@gmail.com> 1.0.3-1
- Oops forgot to modify path for .cluster-membership and .cluster-membership-
  lock chown cmd (jinmaster923@gmail.com)
- Added additional selinux rule for /srv/pulp (jinmaster923@gmail.com)
- Added selinux rules to spec file. (jinmaster923@gmail.com)
- Update import paths (jinmaster923@gmail.com)
- Reorganize %%file section to remove files that are listed twice.
  (jinmaster923@gmail.com)
- Moved all code to src/cds folder. Adjusted cds.spec accordingly.
  (jinmaster923@gmail.com)
- Change location from /var/lib/pulp-cds to /var/lib/pulp
  (jinmaster923@gmail.com)
- More changes to etc/pki/pulp/content folder. (jinmaster923@gmail.com)
- Corect cp error for etc/pki/pulp/content folder. (jinmaster923@gmail.com)

* Tue Jul 22 2014 David Gao <jinmaster923@gmail.com> 1.0.2-1
- Bumping version to 1.0.1 (jinmaster923@gmail.com)

* Tue Jul 22 2014 David Gao <jinmaster923@gmail.com>
- Initial update for producing rsync list based on repo ids provided.
  (jinmaster923@gmail.com)
- Adding test code for generating a list of files to rsync
  (jwmatthews@gmail.com)
- Moved cds unit tests to unit dir, so we may introduce integration tests
  (jwmatthews@gmail.com)
- Restructing unit tests for CDS (jwmatthews@gmail.com)
- Created /etc/pki/pulp/content folder (jinmaster923@gmail.com)
- Update to the latest version of repo_auth.wsgi (jinmaster923@gmail.com)
- Corrected some python errors (jinmaster923@gmail.com)
- Corrected new import path (jinmaster923@gmail.com)
- Initial modifications for permission issues. (jinmaster923@gmail.com)
- Added lb.wsgi Added NullHandler to handle situations where apache does not
  have logging handler. (jinmaster923@gmail.com)
- Re-add lb content back to conf file (jinmaster923@gmail.com)
- Correct typo (jinmaster923@gmail.com)
- Removed cds api section in pulp-cds.conf Added paths needed to be used for
  CDS (jinmaster923@gmail.com)
- Oops, correct cp path mistake from last commit (jinmaster923@gmail.com)
- Added python src files. (jinmaster923@gmail.com)
- Automatic commit of package [pulp-v2-cds] release [1.0.1-1].
  (jinmaster923@gmail.com)
- Initial commit for cds rpm work. (jinmaster923@gmail.com)
- Initialized to use tito. (jinmaster923@gmail.com)
