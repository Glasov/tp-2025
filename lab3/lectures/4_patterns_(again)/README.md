# Поведенческие и структурные паттерны проектирования

## Поведенческие паттерны проектирования

Поведенческие паттерны определяют механизмы взаимодействия между объектами и распределения обязанностей между ними.

Их тоже существует много, но в этой лекции рассмотрим только:

- Strategy (стратегия)
- Responsibility chain (цепочка обязанностей)
- Iterator (итератор)

### Strategy (стратегия)

Паттерн "Стратегия" — это поведенческий паттерн проектирования, который позволяет определить семейство алгоритмов, инкапсулировать каждый из них и сделать их взаимозаменяемыми.

Это позволяет изменять алгоритмы независимо от клиентов, которые ими пользуются.

#### Основные части паттерна "Стратегия"

* Strategy (Стратегия): Интерфейс или абстрактный класс, который определяет метод для выполнения алгоритма.
* ConcreteStrategy (Конкретная стратегия): Конкретные реализации интерфейса или абстрактного класса стратегии. Каждая реализация представляет собой конкретный алгоритм.
* Context (Контекст): Класс, который использует стратегию. Он содержит ссылку на объект стратегии и вызывает метод стратегии для выполнения алгоритма.

В качестве использования паттерна "стратегия" рассмотрим реализации различных алгоритмов сортировки.

Интерфейс стратегии:
```java
public interface SortingStrategy {
    void sort(int[] array);
}
```

Реализация конкретных стратегий:
```java
public class BubbleSortStrategy implements SortingStrategy {
    @Override
    public void sort(int[] array) {
        // Реализация сортировки пузырьком
        System.out.println("Sorting using Bubble Sort");
    }
}

public class QuickSortStrategy implements SortingStrategy {
    @Override
    public void sort(int[] array) {
        // Реализация быстрой сортировки
        System.out.println("Sorting using Quick Sort");
    }
}
```

Создание контекта:
```java
public class Sorter {
    private SortingStrategy strategy;

    public void setStrategy(SortingStrategy strategy) {
        this.strategy = strategy;
    }

    public void sortArray(int[] array) {
        strategy.sort(array);
    }
}
```

Пример использования:
```java
public class Main {
    public static void main(String[] args) {
        Sorter sorter = new Sorter();

        // Использование стратегии сортировки пузырьком
        sorter.setStrategy(new BubbleSortStrategy());
        int[] array1 = {5, 3, 8, 4, 2};
        sorter.sortArray(array1);

        // Использование стратегии быстрой сортировки
        sorter.setStrategy(new QuickSortStrategy());
        int[] array2 = {5, 3, 8, 4, 2};
        sorter.sortArray(array2);
    }
}
```

### Responsibility chain (цепочка обязанностей)

Поведенческий паттерн проектирования, который позволяет передавать запросы по цепочке обработчиков.

Каждый обработчик решает, может ли он обработать запрос сам или нужно передать его следующему обработчику в цепочке, запросы передаются по цепочке обработчиков до тех пор, пока один из них не обработает запрос

```Java
interface Handler {
    void handleRequest(Request request);
    void setNextHandler(Handler nextHandler);
}

// Конкретный обработчик A
class ConcreteHandlerA implements Handler {
    private Handler nextHandler;

    @Override
    public void handleRequest(Request request) {
        if (request.getType() == RequestType.TYPE_A) {
            System.out.println("ConcreteHandlerA handled the request.");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }

    @Override
    public void setNextHandler(Handler nextHandler) {
        this.nextHandler = nextHandler;
    }
}

// Конкретный обработчик B
class ConcreteHandlerB implements Handler {
    private Handler nextHandler;

    @Override
    public void handleRequest(Request request) {
        if (request.getType() == RequestType.TYPE_B) {
            System.out.println("ConcreteHandlerB handled the request.");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request);
        }
    }

    @Override
    public void setNextHandler(Handler nextHandler) {
        this.nextHandler = nextHandler;
    }
}

// Запрос
class Request {
    private RequestType type;

    public Request(RequestType type) {
        this.type = type;
    }

    public RequestType getType() {
        return type;
    }
}

// Типы запросов. В реальной жизни может быть чем-то типа POST или GET
enum RequestType {
    TYPE_A, TYPE_B
}

// Пример использования
public class Main {
    public static void main(String[] args) {
        Handler handlerA = new ConcreteHandlerA();
        Handler handlerB = new ConcreteHandlerB();

        handlerA.setNextHandler(handlerB);

        Request requestA = new Request(RequestType.TYPE_A);
        Request requestB = new Request(RequestType.TYPE_B);

        handlerA.handleRequest(requestA); // Вывод: ConcreteHandlerA handled the request.
        handlerA.handleRequest(requestB); // Вывод: ConcreteHandlerB handled the request.
    }
}
```

### Iterator (итератор)

Поведенческий паттерн проектирования, который предоставляет способ последовательного доступа к элементам составного объекта (например, коллекции или массиву) независимо от его реализации.

```Java
// Интерфейс итератора
interface Iterator<T> {
    boolean hasNext();
    T next();
}

// Конкретный итератор
class ArrayIterator<T> implements Iterator<T> {
    private T[] items;
    private int position;

    public ConcreteIterator(T[] items) {
        this.items = items;
        this.position = 0;
    }

    @Override
    public boolean hasNext() {
        return position < items.length;
    }

    @Override
    public T next() {
        if (this.hasNext()) {
            return items[position++];
        }
        throw new ArrayIndexOutOfBoundsException(); // либо как-то по-другому обрабатывать этот случай, но лучше бросать ошибку
    }
}
```

## Структурные паттерны проектирования

Структурные паттерны проектирования описывают, как классы и объекты могут быть составлены в более крупные структуры, обеспечивая гибкость и масштабируемость.

Сегодня мы рассмотрим три ключевых паттерна:

* Proxy (прокси)
* Adapter (адаптер)
* Bridge (мост)


### Proxy (прокси)

Proxy — это структурный паттерн проектирования, который предоставляет суррогатный объект вместо реального.

Прокси-класс управляет доступом к реальному объекту, добавляя свою логику (например, кеширование, контроль доступа или отложенную инициализацию).

#### Основные части паттерна "Прокси"
Subject (Субъект): Интерфейс или абстрактный класс для реального объекта и прокси.

RealSubject (Реальный субъект): Класс, представляющий настоящий объект, доступ к которому мы контролируем.

Proxy (Прокси): Класс, который выступает в качестве заместителя реального объекта.

#### Пример

Ситуация: Вы создаёте систему, где некоторым пользователям нужен доступ к ограниченным ресурсам.

Например, вы работаете с базой данных, но хотите ограничить доступ к её некоторым функциям.

Реализация:

Интерфейс работы с базой данных:

```java
public interface Database {
    void query(String sql);
}
```

Реальный класс базы данных:

```java
public class RealDatabase implements Database {
    @Override
    public void query(String sql) {
        System.out.println("Executing query: " + sql);
    }
}
```

Прокси с проверкой доступа:

```java
public class DatabaseProxy implements Database {
    private RealDatabase realDatabase;
    private boolean hasAccess;

    public DatabaseProxy(boolean hasAccess) {
        this.realDatabase = new RealDatabase();
        this.hasAccess = hasAccess;
    }

    @Override
    public void query(String sql) {
        if (hasAccess) {
            realDatabase.query(sql);
        } else {
            System.out.println("Access denied. Query cannot be executed.");
        }
    }
}
```

Использование:

```java
public class Main {
    public static void main(String[] args) {
        Database userDb = new DatabaseProxy(false);
        Database adminDb = new DatabaseProxy(true);

        userDb.query("SELECT FROM users"); // Вывод: Access denied. Query cannot be executed.
        adminDb.query("SELECT FROM users"); // Вывод: Executing query: SELECT FROM users
    }
}
```

### Adapter (адаптер)

Adapter — это структурный паттерн проектирования, который позволяет объектам с несовместимыми интерфейсами работать вместе.

#### Основные части паттерна "Адаптер"

Target (Цель): Интерфейс, ожидаемый клиентом.

Adaptee (Адаптируемый): Класс с несовместимым интерфейсом, который нужно адаптировать.

Adapter (Адаптер): Класс, который реализует интерфейс Target и преобразует запросы клиента в формат, понятный Adaptee.

#### Пример

Интеграция сторонней библиотеки

Ситуация: Вы используете библиотеку для обработки данных, но её интерфейс не совпадает с вашими требованиями.

Реализация:

Сторонний класс библиотеки:

```java
public class ExternalLogger {
    public void logMessage(String msg) {
        System.out.println("External log: " + msg);
    }
}
```

Ваш целевой интерфейс:

```java
public interface Logger {
    void log(String message);
}
```

Адаптер для интеграции:

```java
public class LoggerAdapter implements Logger {
    private ExternalLogger externalLogger;

    public LoggerAdapter(ExternalLogger externalLogger) {
        this.externalLogger = externalLogger;
    }

    @Override
    public void log(String message) {
        externalLogger.logMessage(message); // Адаптируем метод
    }
}
```

Использование:

```java
public class Main {
    public static void main(String[] args) {
        ExternalLogger externalLogger = new ExternalLogger();
        Logger logger = new LoggerAdapter(externalLogger);

        logger.log("This is a test message."); // Вывод: External log: This is a test message.
    }
}
```

### Bridge (мост)

Bridge — это структурный паттерн проектирования, который разделяет абстракцию (интерфейс) и реализацию (конкретные детали) на разные иерархии, чтобы их можно было изменять независимо.

#### Основные части паттерна "Мост"

Abstraction (Абстракция): Базовый интерфейс для управления объектами.

Implementor (Реализатор): Интерфейс для конкретной реализации.

ConcreteImplementor (Конкретный реализатор): Конкретная реализация интерфейса Implementor.

RefinedAbstraction (Расширенная абстракция): Конкретная реализация интерфейса Abstraction.

#### Пример
Устройства вывода данных
Ситуация: Вы разрабатываете систему вывода данных, и ваша архитектура должна поддерживать как разные типы устройств (например, монитор и принтер), так и форматы данных (текст, изображения).

Реализация:

Интерфейс устройства:

```java
public interface Device {
    void print(String data);
}
```

Конкретные устройства:

```java
public class Monitor implements Device {
    @Override
    public void print(String data) {
        System.out.println("Displaying on monitor: " + data);
    }
}

public class Printer implements Device {
    @Override
    public void print(String data) {
        System.out.println("Printing to paper: " + data);
    }
}
```

Абстракция вывода:

```java
public abstract class Output {
    protected Device device;

    public Output(Device device) {
        this.device = device;
    }

    public abstract void render(String data);
}
```

Расширенная абстракция:

```java
public class TextOutput extends Output {
    public TextOutput(Device device) {
        super(device);
    }

    @Override
    public void render(String data) {
        device.print("Text: " + data);
    }
}

public class ImageOutput extends Output {
    public ImageOutput(Device device) {
        super(device);
    }

    @Override
    public void render(String data) {
        device.print("Image: [Binary data: " + data + "]");
    }
}
```

Использование:

```java
public class Main {
    public static void main(String[] args) {
        Device monitor = new Monitor();
        Device printer = new Printer();

        Output textOnMonitor = new TextOutput(monitor);
        Output textOnPrinter = new TextOutput(printer);

        textOnMonitor.render("Hello, world!"); // Вывод: Displaying on monitor: Text: Hello, world!
        textOnPrinter.render("Hello, world!"); // Вывод: Printing to paper: Text: Hello, world!

        Output imageOnMonitor = new ImageOutput(monitor);
        imageOnMonitor.render("101010101"); // Вывод: Displaying on monitor: Image: [Binary data: 101010101]
    }
}
```
