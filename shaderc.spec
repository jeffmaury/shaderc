# Release 2017.2
%global commit          7a23a01742b88329fb2260eda007172135ba25d4
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global snapshotdate    20180924
%global gitversion      beginning-449-g7a23a01

# Need to keep this in sync with spirv-tools
%global spirv_commit    f508896d6487d09f5c9a2a3835595446fec0791a

Name:           shaderc
Version:        2017.2
Release:        1%{?dist}
Summary:        A collection of tools, libraries, and tests for Vulkan shader compilation

License:        ASL 2.0
URL:            https://github.com/google/shaderc
Source0:        %url/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

# https://github.com/google/shaderc/pull/463
Patch0:         https://patch-diff.githubusercontent.com/raw/google/shaderc/pull/463.patch#/0001-Fix-the-link-order-of-libglslang-and-libHLSL.patch
# https://github.com/google/shaderc/pull/493
Patch1:         https://patch-diff.githubusercontent.com/raw/google/shaderc/pull/493.patch#/0001-Add-SONAME-version-to-the-library.patch
# Patch to unbundle 3rd party code
Patch2:         0001-Drop-third-party-code-in-CMakeLists.txt.patch

BuildRequires:  cmake3
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  python3-devel
BuildRequires:  glslang-devel
BuildRequires:  spirv-headers-devel
BuildRequires:  spirv-tools
BuildRequires:  spirv-tools-devel

%description
A collection of tools, libraries and tests for shader compilation. 

Shaderc aims to to provide:
 - a command line compiler with GCC- and Clang-like usage, for better 
   integration with build systems
 - an API where functionality can be added without breaking existing clients
 - an API supporting standard concurrency patterns across multiple 
   operating systems
 - increased functionality such as file #include support


%package    -n  glslc
Summary:        A command line compiler for GLSL/HLSL to SPIR-V

%description -n glslc
A command line compiler for GLSL/HLSL to SPIR-V.


%package    -n  libshaderc
Summary:        A library for compiling shader strings into SPIR-V

%description -n libshaderc
A library for compiling shader strings into SPIR-V.


%package -n     libshaderc-devel
Summary:        Development files for libshaderc
Requires:       libshaderc%{?_isa} = %{version}-%{release}

%description -n libshaderc-devel
A library for compiling shader strings into SPIR-V.

Development files for libshaderc.


%package -n     libshaderc-static
Summary:        A library for compiling shader strings into SPIR-V (static libraries)

%description -n libshaderc-static
A library for compiling shader strings into SPIR-V.

Static libraries for libshaderc.


%prep
%autosetup -p1 -n %{name}-%{commit}

rm -rf third_party

# Stolen from Gentoo
# Create build-version.inc since we want to use our packaged 
# SPIRV-Tools and glslang
echo \"shaderc $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\?' CHANGES) %{gitversion}\" \
        > glslc/src/build-version.inc
echo \"spirv-tools $(grep -m1 -o '^v[[:digit:]]\{4\}\.[[:digit:]]\(-dev\)\?' /usr/share/doc/spirv-tools/CHANGES) %{spirv_commit}\" \
        >> glslc/src/build-version.inc
echo \"glslang \'\'\" >> glslc/src/build-version.inc


%build
mkdir %_target_platform
cd %_target_platform
# We disable the tests because they don't work with our unbundling of 3rd party.
# See https://github.com/google/shaderc/issues/470
%cmake3 -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        -DCMAKE_SKIP_RPATH=True \
        -DSHADERC_SKIP_TESTS=True \
        -DPYTHON_EXE=%{__python3} \
        -GNinja ..
%ninja_build


%install
%ninja_install -C %_target_platform


%check
ctest -V


%files -n glslc
%doc glslc/README.asciidoc
%license LICENSE
%{_bindir}/glslc


%files -n libshaderc
%doc AUTHORS CHANGES CONTRIBUTORS README.md
%license LICENSE
%{_libdir}/libshaderc_shared.so.1*


%files -n libshaderc-devel
%{_includedir}/%{name}/
%{_libdir}/libshaderc_shared.so


%files -n libshaderc-static
%license LICENSE
%{_libdir}/libshaderc.a
%{_libdir}/libshaderc_combined.a
%{_libdir}/libshaderc_util.a


%changelog
* Mon Sep 24 2018 Robert-André Mauchin <zebob.m@gmail.com> - 2017.2-1
- Initial build

