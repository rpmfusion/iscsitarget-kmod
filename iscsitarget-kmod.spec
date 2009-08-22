# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:           iscsitarget-kmod
Version:        0.4.17
Release:        2%{?dist}.20
Epoch:          1
Summary:        iscsitarget kernel modules

Group:          System Environment/Kernel
License:        GPLv2
URL:            http://sourceforge.net/projects/iscsitarget/
Source0:        http://dl.sf.net/iscsitarget/iscsitarget-%{version}.tar.gz
Patch0:         iscsitarget-0.4.17-2.6.29.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# needed for plague to make sure it builds for i586 and i686
ExclusiveArch:  i586 i686 x86_64 ppc ppc64

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  %{_bindir}/kmodtool
%{!?kernels:BuildRequires: buildsys-build-rpmfusion-kerneldevpkgs-%{?buildforkernels:%{buildforkernels}}%{!?buildforkernels:current}-%{_target_cpu} }
# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
Kernel module for a kernel-based open source iSCSI target.


%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

# go
%setup -q -c -T -a 0
pushd iscsitarget-%{version}
%patch0 -p0 -b .2.6.29
popd

for kernel_version in %{?kernel_versions}; do
    cp -a iscsitarget-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version in %{?kernel_versions}; do
    make -C "_kmod_build_${kernel_version%%___*}" KSRC="${kernel_version##*___}" patch
    make -C "${kernel_version##*___}" SUBDIRS="${PWD}/_kmod_build_${kernel_version%%___*}"/kernel modules
done


%install
rm -rf $RPM_BUILD_ROOT

for kernel_version in %{?kernel_versions}; do
    install -D -m 755 _kmod_build_${kernel_version%%___*}/kernel/iscsi_trgt.ko \
        $RPM_BUILD_ROOT%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/iscsi_trgt.ko
done

%{?akmod_install}


%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Sat Aug 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.20
- rebuild for new kernels

* Sat Aug 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.19
- rebuild for new kernels

* Fri Aug 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.18
- rebuild for new kernels

* Fri Jul 31 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.17
- rebuild for new kernels

* Tue Jul 14 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.16
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.15
- rebuild for new kernels

* Sun Jun 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.14
- rebuild for new kernels

* Thu May 28 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.13
- rebuild for new kernels

* Wed May 27 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.12
- rebuild for new kernels

* Thu May 21 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.11
- rebuild for new kernels

* Wed May 13 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.10
- rebuild for new kernels

* Tue May 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.9
- rebuild for new kernels

* Sat May 02 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.8
- rebuild for new kernels

* Sun Apr 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.7
- rebuild for new kernels

* Sun Apr 05 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.6
- rebuild for new kernels

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-2.5
- rebuild for new F11 features

* Sun Feb 15 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-1.5
- rebuild for latest Fedora kernel;

* Sun Feb 01 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-1.4
- rebuild for latest Fedora kernel;

* Sun Jan 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-1.3
- rebuild for latest Fedora kernel;

* Sun Jan 18 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-1.2
- rebuild for latest Fedora kernel;

* Sun Jan 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.17-1.1
- rebuild for latest Fedora kernel;

* Mon Jan 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 1:0.4.17-1
- Bump to latest upstream version
- Fix for 2.6.29

* Sun Jan 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-42.svn147.3
- rebuild for latest Fedora kernel;

* Sun Dec 28 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-42.svn147.2
- rebuild for latest Fedora kernel;

* Sat Dec 27 2008 Hans de Goede <hdegoede@redhat.com> - 1:0.4.15-42.svn147.1
- Fix compilation with 2.6.28 kernel

* Sun Dec 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.11
- rebuild for latest Fedora kernel;

* Sun Dec 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.10
- rebuild for latest Fedora kernel;

* Sat Nov 22 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.9
- rebuild for latest Fedora kernel;

* Wed Nov 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.8
- rebuild for latest Fedora kernel;

* Tue Nov 18 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.7
- rebuild for latest Fedora kernel;

* Fri Nov 14 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.6
- rebuild for latest Fedora kernel;

* Sun Nov 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.5
- rebuild for latest Fedora kernel;

* Sun Nov 02 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.4
- rebuild for latest rawhide kernel;

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.3
- rebuild for latest rawhide kernel; enable ppc and ppc64 again

* Sun Oct 19 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.2
- rebuild for latest rawhide kernel

* Fri Oct 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-41.svn147.1
- rebuild for rpm fusion

* Wed Oct 01 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-40.svn147
- rebuild for new kernels

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-39.svn147
- temporary disable ppc due to http://bugzilla.kernel.org/show_bug.cgi?id=11143

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-38.svn147
- rebuild for new kernels
- add patch iscsitarget-0.4.15-types.h.patch from hansg

* Sat Aug 16 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-37.svn147
- rebuild for new kernels

* Thu Jul 24 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.4.15-36
- rebuild for new Fedora kernels

* Tue Jul 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.4.15-35
- rebuild for new Fedora kernels

* Wed Jul 02 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.4.15-34
- rebuild for new Fedora kernels

* Fri Jun 13 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.4.15-33
- rebuild for new Fedora kernels

* Fri Jun 06 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.4.15-32
- rebuild for new Fedora kernels

* Thu May 15 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0.4.15-31
- rebuild for new Fedora kernels

* Sun May 04 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1:0.4.15-30.svn142
- build for f9

* Sat Feb 16 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1:0.4.15-9.svn142
- fix typo

* Thu Feb 14 2008 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.4.15-8.svn147
- Fix compilation for 2.6.24

* Sat Jan 26 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1:0.4.15-7.svn142
- rebuild for new kmodtools, akmod adjustments

* Mon Jan 21 2008 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1:0.4.15-6.svn142
- build akmods package

* Sun Dec 09 2007 Lubomir Kundrak <lkundrak@redhat.com> - 1:0.4.15-5.svn142
- Correct versioning, bump epoch
- Comment on how the svn142 patch was created

* Wed Dec 05 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.4.15.svn142-4
- Convert to kmod2

* Sun Nov 11 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.4.15.svn142-2
- Added make patch before building, to fix builds for 2.6.18 kernels and earlier

* Thu Nov 08 2007 Lubomir Kundrak <lkundrak@redhat.com> - 0.4.15.svn142-1
- Initial package
