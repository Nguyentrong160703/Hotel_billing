# Import các module cần thiết
from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time

# Danh sách các danh mục menu
menu_category = ["Tea & Coffee","Beverages","Fast Food","Starters","Main Course","Dessert"]

# Từ điển liên kết danh mục menu với tên file
menu_category_dict = {
    "Tea & Coffee":"1 Tea & Coffee.txt",
    "Beverages":"2 Beverages.txt",
    "Fast Food":"3 Fast Food.txt",
    "Starters":"4 Starters.txt",
    "Main Course":"5 Main Course.txt",
    "Dessert":"6 Dessert.txt"
}

# Danh sách đơn hàng
order_dict = {}
for i in menu_category:
    order_dict[i] = {}

# Thiết lập thư mục làm việc là thư mục hiện tại của file
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def load_menu():
    '''Hàm để tải danh sách menu'''
    menuCategory.set("")  # Xóa giá trị trong menuCategory
    menu_tabel.delete(*menu_tabel.get_children())  # Xóa nội dung hiện tại trong bảng menu_tabel
    menu_file_list = os.listdir("Menu")  # Lấy danh sách tệp tin trong thư mục "Menu"
    for file in menu_file_list:
        f = open("Menu\\" + file , "r")  # Mở tệp tin
        category=""
        while True:
            line = f.readline()
            if(line==""):
                menu_tabel.insert('',END,values=["","",""])  # Thêm dòng trống vào bảng menu_tabel
                break
            elif (line=="\n"):
                continue
            elif(line[0]=='#'):
                category = line[1:-1]  # Đặt giá trị cho biến category từ dòng bắt đầu bằng "#"
                name = "\t\t"+line[:-1]  # Đặt giá trị cho biến name với khoảng trắng phía trước từ dòng bắt đầu bằng "#"
                price = ""
            elif(line[0]=='*'):
                name = line[:-1]  # Đặt giá trị cho biến name từ dòng bắt đầu bằng "*"
                price = ""
            else:
                name = line[:line.rfind(" ")]  # Đặt giá trị cho biến name từ dòng có định dạng "tên giá"
                price = line[line.rfind(" ")+1:-3]  # Đặt giá trị cho biến price từ dòng có định dạng "tên giá"
            
            menu_tabel.insert('',END,values=[name,price,category])  # Thêm dòng mới vào bảng menu_tabel

def load_order():
    '''Hàm để tải danh sách đơn hàng'''
    order_tabel.delete(*order_tabel.get_children())  # Xóa nội dung hiện tại trong bảng order_tabel
    for category in order_dict.keys():
        if order_dict[category]!={}:
            for item in order_dict[category].keys():
                order_tabel.insert('',END,values=[item,order_dict[category][item]["price"],order_dict[category][item]["quantity"],order_dict[category][item]["total"]])  # Thêm dòng mới vào bảng order_tabel

def add_button_operation():
    ''' Hàm xử lý khi nhấn nút "Add" '''
    item_name = itemName.get()  # Lấy giá trị từ trường nhập liệu itemName
    item_price = itemPrice.get()  # Lấy giá trị từ trường nhập liệu itemPrice
    item_quantity = itemQuantity.get()  # Lấy giá trị từ trường nhập liệu itemQuantity
    item_category = menuCategory.get()  # Lấy giá trị từ combobox menuCategory
    
    if item_name=="" or item_price=="" or item_quantity=="" or item_category=="":
        tmsg.showinfo("Error","Please fill in all the fields.")  # Hiển thị thông báo lỗi nếu có trường nhập liệu không được điền đầy đủ
    else:
        # Kiểm tra xem mục đã tồn tại trong danh sách đơn hàng hay chưa
        if item_name in order_dict[item_category]:
            tmsg.showinfo("Error","Item already exists in the order.")  # Hiển thị thông báo lỗi nếu mục đã tồn tại trong danh sách đơn hàng
        else:
            # Thêm mục vào danh sách đơn hàng
            order_dict[item_category][item_name] = {
                "price": item_price,
                "quantity": item_quantity,
                "total": str(float(item_price)*int(item_quantity))
            }
            
            # Xóa giá trị trong các trường nhập liệu
            itemName.set("")
            itemPrice.set("")
            itemQuantity.set("")
            menuCategory.set("")
            
            # Tải lại danh sách đơn hàng
            load_order()
            
            # Cập nhật tổng giá trị của đơn hàng
            update_total_price()

def load_item_from_menu(event):
    '''Hàm để tải thông tin mục từ bảng menu'''
    selected_row = menu_tabel.selection()  # Lấy dòng được chọn từ bảng menu_tabel
    if len(selected_row) != 0:
        item = menu_tabel.item(selected_row[0])['values']
        itemName.set(item[0])  # Đặt giá trị cho trường nhập liệu itemName
        itemPrice.set(item[1])  # Đặt giá trị cho trường nhập liệu itemPrice
        menuCategory.set(item[2])  # Đặt giá trị cho combobox menuCategory

def load_item_from_order(event):
    '''Hàm để tải thông tin mục từ bảng đơn hàng'''
    selected_row = order_tabel.selection()  # Lấy dòng được chọn từ bảng order_tabel
    if len(selected_row) != 0:
        item = order_tabel.item(selected_row[0])['values']
        itemName.set(item[0])  # Đặt giá trị cho trường nhập liệu itemName
        itemPrice.set(item[1])  # Đặt giá trị cho trường nhập liệu itemPrice
        itemQuantity.set(item[2])  # Đặt giá trị cho trường nhập liệu itemQuantity

def delete_button_operation():
    '''Hàm xử lý khi nhấn nút "Delete"'''
    item_name = itemName.get()  # Lấy giá trị từ trường nhập liệu itemName
    item_category = menuCategory.get()  # Lấy giá trị từ combobox menuCategory
    
    if item_name=="" or item_category=="":
        tmsg.showinfo("Error","Please select an item to delete.")  # Hiển thị thông báo lỗi nếu không có mục nào được chọn
    else:
        # Kiểm tra xem mục có tồn tại trong danh sách đơn hàng hay không
        if item_name not in order_dict[item_category]:
            tmsg.showinfo("Error","Item does not exist in the order.")  # Hiển thị thông báo lỗi nếu mục không tồn tại trong danh sách đơn hàng
        else:
            # Xóa mục khỏi danh sách đơn hàng
            del order_dict[item_category][item_name]
            
            # Xóa giá trị trong các trường nhập liệu
            itemName.set("")
            itemPrice.set("")
            itemQuantity.set("")
            menuCategory.set("")
            
            # Tải lại danh sách đơn hàng
            load_order()
            
            # Cập nhật tổng giá trị của đơn hàng
            update_total_price()

def update_total_price():
    '''Hàm để cập nhật tổng giá trị của đơn hàng'''
    total = 0
    for category in order_dict.keys():
        for item in order_dict[category].keys():
            total += float(order_dict[category][item]["total"])
    totalPrice.set(total)  # Đặt giá trị cho trường nhập liệu totalPrice

def save_order():
    '''Hàm để lưu đơn hàng'''
    # Tạo tên file dựa trên thời gian hiện tại
    file_name = time.strftime("%Y%m%d-%H%M%S") + ".txt"
    
    # Tạo đường dẫn tới thư mục "Orders" nếu chưa tồn tại
    if not os.path.exists("Orders"):
        os.makedirs("Orders")
    
    # Mở tệp tin để ghi đơn hàng
    f = open("Orders\\" + file_name,"w")
    
    # Ghi thông tin đơn hàng vào tệp tin
    for category in order_dict.keys():
        for item in order_dict[category].keys():
            f.write(category + " - " + item + " - " + order_dict[category][item]["quantity"] + "\n")
    
    # Đóng tệp tin
    f.close()
    
    tmsg.showinfo("Success","Order saved successfully.")  # Hiển thị thông báo thành công khi lưu đơn hàng

# Thiết lập giao diện chương trình
root = Tk()

# Đặt tiêu đề cho cửa sổ chương trình
root.title("Restaurant Management System")

# Thiết lập kích thước cửa sổ chương trình
root.geometry("1000x500")

# Tạo thanh cuộn dọc
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# Tạo bảng hiển thị danh sách menu
menu_tabel = ttk.Treeview(root, columns=("name","price","category"), yscrollcommand=scrollbar.set)
menu_tabel.heading("name",text="Item Name")
menu_tabel.heading("price",text="Price")
menu_tabel.heading("category",text="Category")
menu_tabel['show'] = 'headings'
menu_tabel.pack(side=LEFT, fill=BOTH)

# Thiết lập thanh cuộn cho bảng menu_tabel
scrollbar.config(command=menu_tabel.yview)

# Khi chọn mục từ bảng menu_tabel, gọi hàm load_item_from_menu
menu_tabel.bind('<ButtonRelease-1>', load_item_from_menu)

# Tạo trường nhập liệu và nhãn cho trường nhập liệu itemName
itemName = StringVar()
itemNameEntry = Entry(root, textvariable=itemName)
itemNameEntry.pack()
itemNameLabel = Label(root, text="Item Name")
itemNameLabel.pack()

# Tạo trường nhập liệu và nhãn cho trường nhập liệu itemPrice
itemPrice = StringVar()
itemPriceEntry = Entry(root, textvariable=itemPrice)
itemPriceEntry.pack()
itemPriceLabel = Label(root, text="Price")
itemPriceLabel.pack()

# Tạo trường nhập liệu và nhãn cho trường nhập liệu itemQuantity
itemQuantity = StringVar()
itemQuantityEntry = Entry(root, textvariable=itemQuantity)
itemQuantityEntry.pack()
itemQuantityLabel = Label(root, text="Quantity")
itemQuantityLabel.pack()

# Tạo combobox và nhãn cho combobox menuCategory
menuCategory = StringVar()
menuCategoryCombo = ttk.Combobox(root, textvariable=menuCategory)
menuCategoryCombo['values'] = menu_category
menuCategoryCombo.pack()
menuCategoryLabel = Label(root, text="Category")
menuCategoryLabel.pack()

# Tạo nút "Add" và gán hàm add_button_operation cho sự kiện nhấn nút
addButton = Button(root, text="Add", command=add_button_operation)
addButton.pack()

# Tạo bảng hiển thị danh sách đơn hàng
order_tabel = ttk.Treeview(root, columns=("name","price","quantity","total"), yscrollcommand=scrollbar.set)
order_tabel.heading("name",text="Item Name")
order_tabel.heading("price",text="Price")
order_tabel.heading("quantity",text="Quantity")
order_tabel.heading("total",text="Total")
order_tabel['show'] = 'headings'
order_tabel.pack(side=LEFT, fill=BOTH)

# Thiết lập thanh cuộn cho bảng order_tabel
scrollbar.config(command=order_tabel.yview)

# Khi chọn mục từ bảng order_tabel, gọi hàm load_item_from_order
order_tabel.bind('<ButtonRelease-1>', load_item_from_order)

# Tạo nút "Delete" và gán hàm delete_button_operation cho sự kiện nhấn nút
deleteButton = Button(root, text="Delete", command=delete_button_operation)
deleteButton.pack()

# Tạo trường nhập liệu và nhãn cho trường nhập liệu totalPrice
totalPrice = StringVar()
totalPriceEntry = Entry(root, textvariable=totalPrice, state="readonly")
totalPriceEntry.pack()
totalPriceLabel = Label(root, text="Total Price")
totalPriceLabel.pack()

# Tạo nút "Save Order" và gán hàm save_order cho sự kiện nhấn nút
saveButton = Button(root, text="Save Order", command=save_order)
saveButton.pack()

# Tải danh sách menu
load_menu()

# Tải danh sách đơn hàng
load_order()

# Cập nhật tổng giá trị của đơn hàng
update_total_price()

# Chạy chương trình
root.mainloop()