%{?_javapackages_macros:%_javapackages_macros}
# set to 0 provides a minimal test suite
%global with_tests 0

Name:          openjpa
Version:       2.2.2
Release:       5.0%{?dist}
Summary:       Java Persistence 2.0 API

# For a breakdown of the licensing, see NOTICE file
License:       ASL 2.0 and CDDL
Url:           http://openjpa.apache.org/
Source0:       http://www.apache.org/dist/openjpa/%{version}/apache-%{name}-%{version}-source.zip
# fix test failure
Patch0:        %{name}-2.2.0-persistence-jdbc-DynamicEnhancementSuite.patch

BuildRequires: java-devel
%if 0%{?fedora}
%else
BuildRequires: jmock
%endif

BuildRequires: apache-rat-plugin
BuildRequires: buildnumber-maven-plugin
BuildRequires: javacc-maven-plugin
BuildRequires: maven-local
BuildRequires: maven-antrun-plugin
BuildRequires: maven-dependency-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-remote-resources-plugin
BuildRequires: maven-site-plugin
BuildRequires: maven-surefire-provider-junit4

# maven-antrun-plugin deps
BuildRequires: ant-contrib
BuildRequires: ant-jsch

BuildRequires: ant
BuildRequires: apache-commons-collections
BuildRequires: apache-commons-dbcp
BuildRequires: apache-commons-lang
BuildRequires: apache-commons-logging
BuildRequires: apache-commons-pool
BuildRequires: bval
BuildRequires: felix-osgi-core
BuildRequires: geronimo-jms
BuildRequires: geronimo-jta
BuildRequires: geronimo-validation
BuildRequires: glassfish-jaxb
BuildRequires: glassfish-jaxb-api
BuildRequires: hibernate-jpa-2.0-api
BuildRequires: hsqldb1
BuildRequires: log4j
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
BuildRequires: mvn(org.apache.maven:maven-project)
BuildRequires: mvn(org.codehaus.plexus:plexus-utils)
BuildRequires: objectweb-asm
BuildRequires: plexus-utils
BuildRequires: postgresql-jdbc
BuildRequires: serp
BuildRequires: slf4j
BuildRequires: tomcat-servlet-3.0-api

# test deps
BuildRequires: apache-commons-jci-rhino
BuildRequires: derby
BuildRequires: httpunit
BuildRequires: jmock
#BuildRequires: jtds
BuildRequires: junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: mysql-connector-java
BuildRequires: regexp
BuildRequires: simple-jndi

BuildArch:     noarch

%description
OpenJPA is Apache's implementation of Sun's Java Persistence 2.0 API
(JSR-317 JPA 2.0) specification for the transparent persistence of
Java objects.

It is an object-relational mapping (ORM) solution for the Java language,
which simplifies storing objects in databases.

%package tools
Summary:       OpenJPA tools - Maven Plugin

%description tools
OpenJPA tasks for enhancing, SQL creation and
schema mapping creation using Apache maven.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n apache-openjpa-%{version}-source
find . -name "*.class" -delete
find . -name "*.jar" -delete
# openjpa-kernel/internal-repository/com/ibm/websphere/websphere_uow_api/0.0.1/websphere_uow_api-0.0.1.jar
%patch0 -p0

%pom_remove_plugin :docbkx-maven-plugin
%pom_remove_plugin :maven-checkstyle-plugin
%pom_remove_plugin :findbugs-maven-plugin
%pom_remove_plugin :ianal-maven-plugin
%pom_remove_plugin :taglist-maven-plugin

%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='ydoc-profile']"

%pom_remove_dep net.sourceforge.findbugs:annotations

%pom_remove_dep org.apache.geronimo.specs:geronimo-jpa_2.0_spec
%pom_xpath_inject "pom:project/pom:dependencyManagement/pom:dependencies" "
  <dependency>
    <groupId>org.hibernate.javax.persistence</groupId>
    <artifactId>hibernate-jpa-2.0-api</artifactId>
    <version>1.0.1.Final</version>
  </dependency>"
%pom_remove_dep org.apache.bval:org.apache.bval.bundle
%if 0%{?fedora}
%pom_xpath_inject "pom:project/pom:dependencyManagement/pom:dependencies" "
  <dependency>
    <groupId>org.apache.bval</groupId>
    <artifactId>bval-core</artifactId>
    <version>0.5</version>
  </dependency>
  <dependency>
    <groupId>org.apache.bval</groupId>
    <artifactId>bval-jsr303</artifactId>
    <version>0.5</version>
  </dependency>"
%else
%pom_xpath_inject "pom:project/pom:dependencyManagement/pom:dependencies" "
  <dependency>
    <groupId>org.apache.bval</groupId>
    <artifactId>bval-core</artifactId>
    <version>0.5</version>
  </dependency>"
%endif

%pom_remove_dep com.ibm.websphere:websphere_uow_api openjpa-kernel
# require non free com.ibm.websphere websphere_uow_api 0.0.1
rm openjpa-kernel/src/main/java/org/apache/openjpa/ee/WASRegistryManagedRuntime.java
rm openjpa-kernel/src/main/java/org/apache/openjpa/ee/AutomaticManagedRuntime.java

for p in kernel persistence; do
%pom_remove_dep org.osgi:org.osgi.core openjpa-${p}
%pom_xpath_inject "pom:project/pom:dependencies" "
  <dependency>
    <groupId>org.apache.felix</groupId>
    <artifactId>org.osgi.core</artifactId>
    <version>1.4.0</version>
    <scope>provided</scope>
  </dependency>" openjpa-${p}
done

for p in openjpa-jest \
  openjpa-persistence \
  openjpa-tools/openjpa-maven-plugin \
  openjpa-tools/openjpa-maven-plugin/src/it/default_settings \
  openjpa-tools/openjpa-maven-plugin/src/it/dependingArtifact \
  openjpa-tools/openjpa-maven-plugin/src/it/nonDefaultPersistenceXml \
  openjpa-tools/openjpa-maven-plugin/src/it/testDependencies \
  ; do
%pom_remove_dep org.apache.geronimo.specs:geronimo-jpa_2.0_spec ${p}
%pom_xpath_inject "pom:project/pom:dependencies" "
  <dependency>
    <groupId>org.hibernate.javax.persistence</groupId>
    <artifactId>hibernate-jpa-2.0-api</artifactId>
    <version>1.0.1.Final</version>
  </dependency>" ${p}
done

%pom_remove_dep org.apache.geronimo.specs:geronimo-jpa_2.0_spec openjpa-slice
%pom_xpath_inject "pom:project/pom:dependencies" "
  <dependency>
    <groupId>org.hibernate.javax.persistence</groupId>
    <artifactId>hibernate-jpa-2.0-api</artifactId>
    <version>1.0.1.Final</version>
    <scope>test</scope>
  </dependency>" openjpa-slice

%pom_remove_dep org.apache.bval:org.apache.bval.bundle openjpa-tools/openjpa-maven-plugin
%if 0%{?fedora}
%pom_xpath_inject "pom:project/pom:dependencies" "
  <dependency>
    <groupId>org.apache.bval</groupId>
    <artifactId>bval-core</artifactId>
    <version>0.5</version>
  </dependency>
  <dependency>
    <groupId>org.apache.bval</groupId>
    <artifactId>bval-jsr303</artifactId>
    <version>0.5</version>
  </dependency>" openjpa-tools/openjpa-maven-plugin
%else
%pom_xpath_inject "pom:project/pom:dependencies" "
  <dependency>
    <groupId>org.apache.bval</groupId>
    <artifactId>bval-core</artifactId>
    <version>0.5</version>
  </dependency>" openjpa-tools/openjpa-maven-plugin
%endif
  
# remove testing profiles for unavailable drivers: 
# db2jcc informix-driver jcc-driver jdbc-driver jdbc-oracle jtds sqljdbc
#%%pom_xpath_remove "pom:profiles/pom:profile[pom:id='test-mysql']" openjpa-persistence-jdbc
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-sybase-jconnect']" openjpa-persistence-jdbc
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-soliddb']" openjpa-persistence-jdbc
for p in openjpa-persistence-jdbc openjpa-persistence-locking; do
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-custom']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-custom2']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-db2-jcc']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-derbyjcc']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-ids-jcc']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-ids-informix']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-ingres']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-mssql']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-oracle']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-sqlserver']" ${p}
%pom_xpath_remove "pom:project/pom:profiles/pom:profile[pom:id='test-sybase']" ${p}
done

# in f17 buildnumber dont work
#%%pom_remove_plugin org.codehaus.mojo:buildnumber-maven-plugin


%pom_disable_module openjpa
%pom_disable_module openjpa-all
%pom_disable_module openjpa-examples
%pom_disable_module openjpa-integration
%pom_disable_module openjpa-project
%pom_disable_module openbooks openjpa-examples

# break build in f19
%pom_remove_plugin :maven-invoker-plugin openjpa-tools/openjpa-maven-plugin

%pom_xpath_inject "pom:project/pom:dependencies/pom:dependency[pom:artifactId='hsqldb']" "
<version>1</version>" openjpa-jdbc

sed -i 's|<hsqldb.version>1.8.0.10</hsqldb.version>|<hsqldb.version>1</hsqldb.version>|' pom.xml

#%%pom_remove_dep org.apache.maven:maven-project openjpa-tools/openjpa-maven-plugin
#%%pom_add_dep org.apache.maven:maven-core openjpa-tools/openjpa-maven-plugin

%build
%mvn_package ":%{name}-tools" tools
%mvn_package ":%{name}-maven-plugin" tools
# test random fails
# force tomcat 7.x apis
%mvn_build -- \
%if %{with_tests}
  -Ptest-derby \
%else
  -Dtest=false \
%endif
  -DfailIfNoTests=false \
  -Dmaven.test.failure.ignore=true \
  -Dmaven.local.depmap.file="%{_mavendepmapfragdir}/tomcat-tomcat-servlet-api" \
  process-resources

%install
%mvn_install

mkdir -p %{buildroot}%{_sysconfdir}/ant.d
echo "ant %{name}/%{name}-jdbc %{name}/%{name}-kernel %{name}/%{name}-lib" > %{name}-ant
install -p -m 644 %{name}-ant %{buildroot}%{_sysconfdir}/ant.d/%{name}

%files -f .mfiles
%dir %{_javadir}/%{name}
%config(noreplace) %{_sysconfdir}/ant.d/%{name}
%doc CHANGES.txt LICENSE NOTICE README.txt RELEASE-NOTES.html

%files tools -f .mfiles-tools
%doc LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 gil cattaneo <puntogil@libero.it> 2.2.2-4
- fix ant.d script

* Tue Jul 09 2013 gil cattaneo <puntogil@libero.it> 2.2.2-3
- switch to XMvn
- minor changes to adapt to current guideline

* Mon Jun 24 2013 Tomas Radej <tradej@redhat.com> - 2.2.2-2
- B(R) on hsqldb compat package

* Thu May 23 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- update to 2.2.2

* Sun Feb 17 2013 gil cattaneo <puntogil@libero.it> 2.2.1-4
- disabled invoker-plugin in f19

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 2.2.1-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Nov 08 2012 gil cattaneo <puntogil@libero.it> 2.2.1-1
- update to 2.2.1

* Mon Jul 16 2012 gil cattaneo <puntogil@libero.it> 2.2.0-2
- Fixed license tag
- Own directory

* Fri Apr 06 2012 gil cattaneo <puntogil@libero.it> 2.2.0-1
- initial rpm
