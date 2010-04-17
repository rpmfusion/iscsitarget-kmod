# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels newest

Name:           iscsitarget-kmod
Version:        1.4.18
Release:        1%{?dist}.21
Epoch:          1
Summary:        iscsitarget kernel modules

Group:          System Environment/Kernel
License:        GPLv2
URL:            http://sourceforge.net/projects/iscsitarget/
Source0:        http://dl.sf.net/iscsitarget/iscsitarget-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
* Sat Apr 17 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.21
- rebuild for new kernel

* Sat Apr 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.20
- rebuild for new kernel

* Mon Mar 29 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.19
- rebuild for new kernel

* Fri Mar 05 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.18
- rebuild for new kernel

* Mon Mar 01 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.17
- rebuild for new kernel

* Sun Feb 28 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.16
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.15
- rebuild for new kernel

* Sat Feb 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.14
- rebuild for new kernel

* Thu Feb 11 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.13
- rebuild for new kernel

* Wed Feb 10 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.12
- rebuild for new kernel

* Sat Jan 30 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.11
- rebuild for new kernel

* Wed Jan 20 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.10
- rebuild for new kernel

* Sat Dec 26 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.9
- rebuild for new kernel

* Thu Dec 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.8
- rebuild for new kernel

* Sun Dec 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.7
- rebuild for new kernel

* Wed Nov 25 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.6
- rebuild for new kernel

* Sun Nov 22 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.5
- rebuild for new kernel, disable i586 builds

* Tue Nov 10 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.4
- rebuild for F12 release kernel

* Mon Nov 09 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.3
- rebuild for new kernels

* Fri Nov 06 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.2
- rebuild for new kernels

* Wed Nov 04 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:1.4.18-1.1
- rebuild for new kernels

* Sun Nov 01 2009 Lubomir Rintel <lkundrak@v3.sk> - 1:1.4.18-1
- Update to newer upstream release
- Remove rebuild changelog entries

* Thu Jul 30 2009 Hans de Goede <hdegoede@redhat.com> - 1:0.4.17-3
- Fix compilation with 2.6.31 kernel

* Mon Jan 05 2009 Lubomir Rintel <lkundrak@v3.sk> - 1:0.4.17-1
- Bump to latest upstream version
- Fix for 2.6.29

* Sat Dec 27 2008 Hans de Goede <hdegoede@redhat.com> - 1:0.4.15-42.svn147.1
- Fix compilation with 2.6.28 kernel

* Sun Oct 26 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1:0.4.15-41.svn147.3
- rebuild for latest rawhide kernel; enable ppc and ppc64 again

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-39.svn147
- temporary disable ppc due to http://bugzilla.kernel.org/show_bug.cgi?id=11143

* Sun Sep 21 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1:0.4.15-38.svn147
- rebuild for new kernels
- add patch iscsitarget-0.4.15-types.h.patch from hansg

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
