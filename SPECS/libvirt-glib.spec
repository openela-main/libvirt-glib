# -*- rpm-spec -*-

%define with_introspection 0
%define with_vala 0

%if 0%{?fedora} >= 15
%define with_introspection 1
%endif
%if 0%{?rhel} > 6
%define with_introspection 1
%endif
%define with_vala %{with_introspection}

%define libvirt_version 1.2.5

Name: libvirt-glib
Version: 3.0.0
Release: 1%{?dist}%{?extra_release}
Summary: libvirt glib integration for events
Group: Development/Libraries
License: LGPLv2+
URL: http://libvirt.org/
Source0: ftp://libvirt.org/libvirt/glib/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: glib2-devel >= 2.38.0
BuildRequires: libvirt-devel >= %{libvirt_version}
%if %{with_introspection}
BuildRequires: gobject-introspection-devel
%if 0%{?fedora} == 12
BuildRequires: gir-repository-devel
%endif
%endif
BuildRequires: libxml2-devel
# Hack due to https://bugzilla.redhat.com/show_bug.cgi?id=613466
BuildRequires: libtool
%if %{with_vala}
BuildRequires: vala-tools
%endif
BuildRequires: intltool

%package devel
Group: Development/Libraries
Summary: libvirt glib integration for events development files
Requires: %{name} = %{version}-%{release}

%package -n libvirt-gconfig
Group: Development/Libraries
Summary: libvirt object APIs for processing object configuration

%package -n libvirt-gobject
Group: Development/Libraries
Summary: libvirt object APIs for managing virtualization hosts

%package -n libvirt-gconfig-devel
Group: Development/Libraries
Summary: libvirt object APIs for processing object configuration development files
Requires: libvirt-gconfig = %{version}-%{release}

%package -n libvirt-gobject-devel
Group: Development/Libraries
Summary: libvirt object APIs for managing virtualization hosts development files
Requires: %{name}-devel = %{version}-%{release}
Requires: libvirt-gconfig-devel = %{version}-%{release}
Requires: libvirt-gobject = %{version}-%{release}
Requires: libvirt-devel >=  %{libvirt_version}

%description
This package provides integration between libvirt and the glib
event loop.

%description devel
This package provides development header files and libraries for
integration between libvirt and the glib event loop.

%description -n libvirt-gconfig
This package provides APIs for processing the object configuration
data

%description -n libvirt-gconfig-devel
This package provides development header files and libraries for
the object configuration APIs.

%description -n libvirt-gobject
This package provides APIs for managing virtualization host
objects

%description -n libvirt-gobject-devel
This package provides development header files and libraries for
managing virtualization host objects

%prep
%setup -q

%build

%if %{with_introspection}
%define introspection_arg --enable-introspection
%else
%define introspection_arg --disable-introspection
%endif

%configure %{introspection_arg}
%__make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%__make install  DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-glib-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-glib-1.0.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gconfig-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gconfig-1.0.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gobject-1.0.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libvirt-gobject-1.0.la

%find_lang %{name}

%check
if ! make %{?_smp_mflags} check; then
  cat tests/test-suite.log || true
  exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n libvirt-gconfig -p /sbin/ldconfig

%postun -n libvirt-gconfig -p /sbin/ldconfig

%post -n libvirt-gobject -p /sbin/ldconfig

%postun -n libvirt-gobject -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING AUTHORS ChangeLog NEWS
%{_libdir}/libvirt-glib-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGLib-1.0.typelib
%endif

%files -n libvirt-gconfig
%{_libdir}/libvirt-gconfig-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGConfig-1.0.typelib
%endif

%files -n libvirt-gobject
%{_libdir}/libvirt-gobject-1.0.so.*
%if %{with_introspection}
%{_libdir}/girepository-1.0/LibvirtGObject-1.0.typelib
%endif

%files devel
%defattr(-,root,root,-)
%doc examples/event-test.c
%{_libdir}/libvirt-glib-1.0.so
%{_libdir}/pkgconfig/libvirt-glib-1.0.pc
%dir %{_includedir}/libvirt-glib-1.0
%dir %{_includedir}/libvirt-glib-1.0/libvirt-glib
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib.h
%{_includedir}/libvirt-glib-1.0/libvirt-glib/libvirt-glib-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGLib-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-glib
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-glib-1.0.vapi
%endif

%files -n libvirt-gconfig-devel
%defattr(-,root,root,-)
%doc examples/event-test.c
%{_libdir}/libvirt-gconfig-1.0.so
%{_libdir}/pkgconfig/libvirt-gconfig-1.0.pc
%dir %{_includedir}/libvirt-gconfig-1.0
%dir %{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig.h
%{_includedir}/libvirt-gconfig-1.0/libvirt-gconfig/libvirt-gconfig-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGConfig-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-gconfig
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-gconfig-1.0.vapi
%endif

%files -n libvirt-gobject-devel
%defattr(-,root,root,-)
%doc examples/event-test.c
%{_libdir}/libvirt-gobject-1.0.so
%{_libdir}/pkgconfig/libvirt-gobject-1.0.pc
%dir %{_includedir}/libvirt-gobject-1.0
%dir %{_includedir}/libvirt-gobject-1.0/libvirt-gobject
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject.h
%{_includedir}/libvirt-gobject-1.0/libvirt-gobject/libvirt-gobject-*.h
%if %{with_introspection}
%{_datadir}/gir-1.0/LibvirtGObject-1.0.gir
%endif
%{_datadir}/gtk-doc/html/Libvirt-gobject
%if %{with_vala}
%{_datadir}/vala/vapi/libvirt-gobject-1.0.deps
%{_datadir}/vala/vapi/libvirt-gobject-1.0.vapi
%endif

%changelog
* Sun May 31 2020 Fabiano Fidêncio <fidencio@redhat.com> 3.0.0-1
- Update to 3.0.0 release
- Resolves: rhbz#1754396 - Provide support for getting "firmwares" info from Domain Capabilities
- Resolves: rhbz#1753670 - Enable bochs-display for UEFI guests (libvirt-glib)

* Fri Oct 12 2018 Fabiano Fidêncio <fidencio@redhat.com> 2.0.0-1
- Update to 2.0.0 release
- Resolves: rhbz#1638818 - Rebase libvirt-glib to 2.0.0

* Mon Oct 30 2017 Marek Kasik <mkasik@redhat.com> - 1.0.0-5
- Enable unit tests
- Resolves: #1502639

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Nov  4 2016 Daniel P. Berrange <berrange@redhat.com> - 1.0.0-1
- Update to 1.0.0 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 16 2015 Daniel P. Berrange <berrange@redhat.com> - 0.2.3-1
- Update to 0.2.3 release

* Tue Aug 18 2015 Kalev Lember <klember@redhat.com> - 0.2.2-1
- Update to 0.2.2 release

* Tue Jun 16 2015 Daniel P. Berrange <berrange@redhat.com> - 0.2.1-1
- Update to 0.2.1 release

* Mon Dec 15 2014 Daniel P. Berrange <berrange@redhat.com> - 0.2.0-1
- Update to 0.2.0 release

* Wed Aug 20 2014 Daniel P. Berrange <berrange@redhat.com> - 0.1.9-1
- Update to 0.1.9 release

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.8-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 21 2014 Daniel P. Berrange <berrange@redhat.com> - 0.1.8-1
- Update to 0.1.8 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul  8 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.7-1
- Update to 0.1.7 release

* Mon Mar 18 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.6-1
- Update to 0.1.6 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Daniel P. Berrange <berrange@redhat.com> - 0.1.5-1
- Update to 0.1.5 release

* Fri Nov 16 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.4-1
- Update to 0.1.4 release

* Mon Oct  8 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.3-1
- Update to 0.1.3 release

* Mon Aug 20 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.2-1
- Update to 0.1.2 release

* Tue Aug  7 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.1-1
- Update to 0.1.1 release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 16 2012 Daniel P. Berrange <berrange@redhat.com> - 0.1.0-1
- Update to 0.1.0 release

* Mon Jun 25 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.9-1
- Update to 0.0.9 release

* Wed May 16 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.0.8-2
- Bump release number (no build pushed until there are more useful changes
  in there)
- Fixed conditional to ensure vala bindings are built for Fedora >= 15
  and for RHEL > 6

* Fri Apr 27 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.8-1
- Update to 0.0.8 release

* Fri Mar 30 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.7-1
- Update to 0.0.7 release

* Tue Mar 06 2012 Christophe Fergeau <cfergeau@redhat.com> - 0.0.6-1
- Update to 0.0.6 release

* Mon Feb 20 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.5-1
- Update to 0.0.5 release

* Thu Jan 12 2012 Daniel P. Berrange <berrange@redhat.com> - 0.0.4-1
- Update to 0.0.4 release

* Mon Dec 19 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.3-1
- Update to 0.0.3 release

* Tue Nov 22 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.2-1
- Update to 0.0.2 release

* Tue Nov 22 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-2
- Remove gjs-devel BR
- Add missing ldconfig post/postun scripts
- Fixed conditional to ensure python is disabled for Fedora >= 15

* Mon Nov 14 2011 Daniel P. Berrange <berrange@redhat.com> - 0.0.1-1
- Initial release

