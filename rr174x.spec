# Conditional build:
%bcond_without	dist_kernel	# allow non-distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_with	verbose		# verbose build (V=1)

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel	0.1
%define		pname	rr174x
%define		basever	2.1
%define		subver	08.0710
%define		_subver	%(echo %{subver} | tr -d .)
Summary:	Driver for HighPoint RocketRAID 174x SATA controller
Name:		%{pname}%{_alt_kernel}
Version:	%{basever}.%{subver}
Release:	%{rel}
License:	Proprietary
Group:		Base/Kernel
Source0:	http://www.highpoint-tech.com/BIOS_Driver/rr1740/Linux/%{pname}-linux-src-v%{basever}-%{_subver}-1311.tar.gz
# Source0-md5:	12763d34c8b725ce0c25e3431745e1ce
Patch0:		%{pname}-cflags.patch
URL:		http://www.highpoint-tech.com/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains Linux driver for HighPoint RocketRAID 174x SATA
controller.

%package -n kernel%{_alt_kernel}-misc-rr174x
Summary:	Linux driver for rr174x
Summary(pl.UTF-8):	Sterownik dla Linuksa do rr174x
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif

%description -n kernel%{_alt_kernel}-misc-rr174x
This is driver for rr174x for Linux.

This package contains Linux module.

%description -n kernel%{_alt_kernel}-misc-rr174x -l pl.UTF-8
Sterownik dla Linuksa do rr174x.

Ten pakiet zawiera moduł jądra Linuksa.

%prep
%setup -q -n %{pname}-linux-src-v%{basever}
%{__sed} -i -e 's,\r$,,' README inc/linux/Makefile.def
%patch -P0 -p1

%build
%if %{with kernel}
pwd=$(pwd)
cd product/rr1740pm/linux
# XXX: fool build macro
touch rr174x.ko
%build_kernel_modules -m rr174x KERNELDIR=$(pwd)/o KERNEL_VER=2.6 HPT_ROOT="$pwd"
# XXX. it didn't build module with above...
%{__make} KERNELDIR=$(pwd)/o
mv -f rr174x{,-dist}.ko
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m product/rr1740pm/linux/rr174x -d kernel/misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-misc-rr174x
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-misc-rr174x
%depmod %{_kernel_ver}

%if %{with kernel}
%files -n kernel%{_alt_kernel}-misc-rr174x
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/misc/*.ko*
%endif
