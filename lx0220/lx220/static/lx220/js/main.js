$(document).on('click','.custom-radio',function () {
    $(this).addClass('active').siblings().removeClass('active');
});
//元数据管理页面表格数据
var arr = [
    {'name':'计算口径','class':'基本信息','choose':'是'},
    {'name':'设计单位','class':'特征信息','choose':'否'},
    {'name':'编制时间','class':'基本信息','choose':'是'},
    {'name':'总层数','class':'特征信息','choose':'否'},
    {'name':'计算口径','class':'基本信息','choose':'是'},
    {'name':'编制时间','class':'基本信息','choose':'是'}
];
//初始化加载数据
function  init() {
    $(".set-metadata-management tbody").empty();
    $.each(arr,function (index,item) {
        $(".set-metadata-management tbody").append(
            `<tr class="data-tr" index="${index}">
        <td>${item.name}</td>
        <td>${item.class}</td>
        <td>${item.choose}</td>
        <td>
        <a index="${index}" href="javascript:;" class="blue mgr22 edit-btn">编辑</a>
        <a index="${index}" href="javascript:;" class="red del-btn">删除</a>
        </td>
    </tr>`
        )
    });
    indexNumber();
}
//排序处理
function indexNumber(){
    $('.set-metadata-management tr').each(function(index, obj){
        $(obj).attr('index',index-1);
    });
}
//清空数据
function empty() {
    $('.add-metadata input').val('');
    $('.add-metadata select option').removeAttr('selected');
    $('.custom-radio:first-child').addClass('active').siblings().removeClass('active');  //radio默认是第一个
}
//初始化
init();
//点击编辑
$('.set-metadata-management').on('click','.edit-btn',function () {
    empty();
    var index = $(this).attr("index");  //添加下标
    var data = arr[index];
    $('.modal-add .title_v3_l').text('编辑元数据');  //修改弹层名称
    $('.modal-add').show(200,function () {
        $('.add-metadata input').val(data.name);
        if(data.class === '基本信息'){   //判断select下拉菜单选择
            $('.add-metadata select option[value="0"]').attr('selected','selected');
        }else {
            $('.add-metadata select option[value="1"]').attr('selected','selected');
        }

        if(data.choose === '是'){   //判断radius选中
                $('.custom-radio:first-child').addClass('active').siblings().removeClass('active');
            }else {
                $('.custom-radio:last-child').addClass('active').siblings().removeClass('active');
            }
    });
    $('.modal-add').one('click','.sure-btn',function (){  //点击确定按钮保存数据
        $('.modal-add').hide(200,function () {
            var text = {     //获取编辑的值
                name:$('.add-metadata input').val(),
                class:$('.add-metadata select option:selected').text(),
                choose:$('.add-metadata .custom-radio.active').text()
            };
            //替换编辑的数据
            data.name = text.name;
            data.class = text.class;
            data.choose = text.choose;
            init();   //重新初始化
        });
    });

});

//点击删除
$('.set-metadata-management').on('click','.del-btn',function () {
    var that = this;
    var index = $(that).attr("index");
    arr.splice(index,1);
    var value = $(that).parents('tr').find('td:eq(0)').text();   //获取标题名称
    $('.modal-tip .ensure-wz>span').text(value);
    $('.modal-tip').show(200,function () {
        $('.modal-tip .sure-btn').click(function () {
             $(".data-tr[index="+index+"]").remove();
            init();
         })
    });
});
 //新增一行
 $('.set-metadata-management').on('click','.save-btn',function () {
     empty();
     $('.modal-add').show(200,function () {
         $('.modal-add .title_v3_l').text('新增元数据');  //修改弹层名称
         $('.modal-add').one('click','.sure-btn',function () {  //点击确定按钮获取数据
             $('.modal').hide(200);
             var text = {
                 name:$('.add-metadata input').val(),
                 class:$('.add-metadata select option:selected').text(),
                 choose:$('.add-metadata .custom-radio.active').text()
             };
             var value = $.trim(text.name); // trim方法删除前后空格
             if(value===''){    //名称不为空
                 alert('请输入名称');
                 return;
             }
             //      var list =
             //          '<tr class="data-tr" index="${index}">'+
             //     '<td>'+text.name+'</td>'+
             //     '<td>'+text.class+'</td>'+
             //     '<td>'+text.choose+'</td>'+
             //     '<td>'+
             //     '<a href="javascript:;" class="blue mgr22 edit-btn">'+'编辑'+'</a>'+
             //     '<a href="javascript:;" class="red del-btn">'+'删除'+'</a>'+
             //     '</td>'+
             // '</tr>';
             //      $(".set-metadata-management tbody").prepend(list);
             arr.push(text);
             init();
         });
     });

 });


//关闭弹层
$(document).on('click','.modal .close',function () {
    $(this).parents('.modal').hide(200);
});

