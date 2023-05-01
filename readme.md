# Project Warehouse

Приложение для учета техники на складе.

Реализованы следующие адреса: 
* http://172.17.0.1:5000/warehouse-report - Вывод отчета о технике в наличии по всем складам
* http://172.17.0.1:5000/technic-report - Вывод отчета о количестве единиц техники 
* http://172.17.0.1:5000/technic-report/histogram - Вывод гистограммы частот остатков техники

Для загрузки образа и запуска достаточно выполнить команды: 
```bash
sudo docker pull kamomem/warehouse
sudo docker run kamomem/warehouse
```
В этом случае произойдет загрузка образа с репозитория docker.
В нем образ расположен по адресу https://hub.docker.com/r/kamomem/warehouse

Для сборки и запуска использовались следующие команды:
```bash
sudo docker build -t kamomem/warehouse .
sudo dockerun -p 8888:5000 -it --rm  kamomem/warehouse
```

При запуске контейнера производится создание базы данных, затем создание и загрузка стартового набора данных
для начала работы. Создаются 5 сотрудников, 5 складов и 100 единиц техники.
Затем, генерируется нормальное распределение количества техники в диапазоне от 0 до 100 для каждой единицы.
Техника случайным образом распределяется между накладными и распределяется по складам. 

Нормальное распределение генерируется случайным образом. При этом идеальное нормальное  
распределение количества товаров гарантируется только при большом количестве товаров. 
При заданном параметре в 100 единиц различной техники возможны отклонения.   


Вариант гистограммы частот по количеству техники может выглядеть следующим образом:


![](/warehouse/static/1.jpg)



Если группировать гистограмму до 10 столбцов то получится:


![](/warehouse/static/3.jpg)


А если  до 5 столбцов то:


![](/warehouse/static/2.jpg)



Таким образом количество товаров генерируется действительно по закону
нормального распределения, однако присутствует погрешность из-за низкого числа единиц техники.

