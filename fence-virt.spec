Name:		fence-virt
Version:	0.2.1
Release:	5%{?dist}
Summary:	A pluggable fencing framework for virtual machines
Group:		System Environment/Base
License:	GPLv2+
URL:		http://voxel.dl.sourceforge.net/project/fence-virt/fence-virt-%{version}.tar.gz
Source0:	%{name}-%{version}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

ExclusiveArch:	i686 x86_64

BuildRequires:	corosynclib-devel clusterlib-devel libvirt-devel
BuildRequires:	openaislib-devel
BuildRequires:	qpid-cpp-client-devel qmf-devel
BuildRequires:	automake autoconf libxml2-devel nss-devel nspr-devel
BuildRequires:	flex bison libuuid-devel
Conflicts:	fence-agents < 3.0.5-2


Patch0: 0001-Make-configure.in-actually-disable-plugins.patch
Patch10: bz561418-1-of-1.patch
Patch11: bz563624-1-of-1.patch
Patch12: bz563626-1-of-1.patch

%description
Fencing agent for virtual machines.


%package -n fence-virtd
Summary:	Daemon which handles requests from fence-virt
Group:		System Environment/Base

%description -n fence-virtd
This package provides the host server framework, fence_virtd,
for fence_virt.  The fence_virtd host daemon is resposible for
processing fencing requests from virtual machines and routing
the requests to the appropriate physical machine for action.


%package -n fence-virtd-multicast
Summary:	Multicast listener for fence-virtd
Group:		System Environment/Base
Requires:	fence-virtd

%description -n fence-virtd-multicast
Provides multicast listener capability for fence-virtd.


%package -n fence-virtd-serial
Summary:	Serial VMChannel listener for fence-virtd
Group:		System Environment/Base
Requires:	libvirt >= 0.6.2
Requires:	fence-virtd

%description -n fence-virtd-serial
Provides serial VMChannel listener capability for fence-virtd.


%package -n fence-virtd-libvirt
Summary:	Libvirt backend for fence-virtd
Group:		System Environment/Base
Requires:	libvirt > 0.6.0
Requires:	fence-virtd

%description -n fence-virtd-libvirt
Provides fence_virtd with a connection to libvirt to fence
virtual machines.  Useful for running a cluster of virtual
machines on a desktop.


%package -n fence-virtd-libvirt-qpid
Summary:	Libvirt-qpid backend for fence-virtd
Group:		System Environment/Base
Requires:	libvirt > 0.6.0
Requires:	fence-virtd libvirt-qpid

%description -n fence-virtd-libvirt-qpid
Provides fence_virtd with a connection to libvirt-qpid to
fence virtual machines.  Libvirt-qpid provies a QMF model
to track VMs across multiple hosts.


%package -n fence-virtd-checkpoint
Summary:	Cluster+Libvirt backend for fence-virtd
Group:		System Environment/Base
Requires:	fence-virtd

%description -n fence-virtd-checkpoint
Provides fence_virtd with a connection to libvirt to fence
virtual machines.  Utilizes corosync's CPG framework to route
requests as well as the AIS Checkpoint API to store virtual
machine states across a cluster and make intelligent decisions
about whether a virtual machine is running.


%prep
%setup -q

%patch0 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

%build
./autogen.sh
%{configure}
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -m 0755 fence_virtd.init %{buildroot}/%{_sysconfdir}/rc.d/init.d/fence_virtd


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING TODO README
%{_sbindir}/fence_virt
%{_sbindir}/fence_xvm
%{_mandir}/man8/fence_virt.*
%{_mandir}/man8/fence_xvm.*

%files -n fence-virtd
%defattr(-,root,root,-)
%{_sbindir}/fence_virtd
%{_sysconfdir}/rc.d/init.d/fence_virtd
%config(noreplace) %{_sysconfdir}/fence_virt.conf
%dir %{_libdir}/%{name}
%{_mandir}/man5/fence_virt.conf.*
%{_mandir}/man8/fence_virtd.*

%files -n fence-virtd-multicast
%defattr(-,root,root,-)
%{_libdir}/%{name}/multicast.so

%files -n fence-virtd-serial
%defattr(-,root,root,-)
%{_libdir}/%{name}/serial.so

%files -n fence-virtd-libvirt
%defattr(-,root,root,-)
%{_libdir}/%{name}/libvirt.so

%files -n fence-virtd-libvirt-qpid
%defattr(-,root,root,-)
%{_libdir}/%{name}/libvirt-qpid.so

%files -n fence-virtd-checkpoint
%defattr(-,root,root,-)
%{_libdir}/%{name}/checkpoint.so

%changelog
* Fri Aug 6 2010 Lon Hohberger <lhh@redhat.com> - 0.2.1-5
- Rebuild against current qmf-client-cpp
  Resolves: rhbz#621889

* Wed May 12 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.2.1-4
- Do not build on ppc and ppc64.
  Resolves: rhbz#590986

* Wed Feb 24 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-3
- Fix spec file due to qpid package renaming and architecture changes
- Don't build on s390 and s390x
- Resolves: rhbz#568003 rhbz#567744

* Wed Feb 10 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-2
- Fix man page location
- Fix metadata output
- Fix arguments to be more consistent with other fencing
  agents
- Resolves: rhbz#561418 rhbz#563624 rhbz#563626

* Fri Jan 15 2010 Lon Hohberger <lhh@redhat.com> 0.2.1-1
- Update to latest upstream version
- Fix bug around status return codes for VMs which are 'off'

* Thu Jan 14 2010 Lon Hohberger <lhh@redhat.com> 0.2-1
- Update to latest upstream version
- Serial & VMChannel listener support
- Static permission map support
- Man pages
- Init script
- Various bugfixes

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0.1.2-1.1
- Rebuilt for RHEL 6

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.2-1
- Update to latest upstream version
- Fix build issue on i686

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1.1-1
- Update to latest upstream version
- Clean up spec file

* Mon Sep 21 2009 Lon Hohberger <lhh@redhat.com> 0.1-2
- Spec file cleanup

* Thu Sep 17 2009 Lon Hohberger <lhh@redhat.com> 0.1-1
- Initial build for rawhide
