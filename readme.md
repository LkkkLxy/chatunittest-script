# 运行步骤

### 1.在项目中pom.xml中添加:

```XML
<plugin>

    <groupId>io.github.ZJU-ACES-ISE</groupId>
    <artifactId>chatunitest-maven-plugin</artifactId>
    <version>1.4.1</version>
    <configuration>
        <!-- 在这里填写你的api-key -->
        <apiKeys>API-KEY</apiKeys>
        <model>deepseek-chat</model>
        <url>https://api.deepseek.com/chat/completions</url>
        <testNumber>5</testNumber>
        <maxRounds>5</maxRounds>
        <minErrorTokens>500</minErrorTokens>
        <temperature>0.5</temperature>
        <topP>1</topP>
        <frequencyPenalty>0</frequencyPenalty>
        <presencePenalty>0</presencePenalty>
        <proxy>${proxy}</proxy>
    </configuration>
</plugin>
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.12</version> 
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>

<dependency>
    <groupId>io.github.ZJU-ACES-ISE</groupId>
    <artifactId>chatunitest-starter</artifactId>
    <version>1.4.0</version>
    <type>pom</type>
</dependency>

```

并填入自己的api-key.

### 2.配置信息
修改script.py中的下列信息：

```
# JACOCO覆盖率分析器路径，改成自己的jar包位置
JACOCO_COVERAGE_JAR_PATH = "/home/othertest/jacoco_analyzer/target/coverage-1.0-SNAPSHOT.jar"
# 测试执行文件，改成自己的exec文件位置
exec_file_path = "/home/othertest/books/target/jacoco.exec"
# 包含目标类文件的目录路径，改成自己的目录路径
class_file_path = "/home/othertest/books/target/classes"
# 测试文件路径，改成自己的测试文件路径
project_path = "/home/othertest/books"
```

### 3.运行脚本:

```
python script.py <class_name>[<return_value>]<method_name>
```

例如：

```python
python script.py "com.aidanwhiteley.books.service.UserService[Optional<User>]createOrUpdateActuatorUser()"
```

覆盖率信息会打印在控制台，所有信息会记录在同目录下的coverage_analyzer.log