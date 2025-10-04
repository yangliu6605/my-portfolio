// 1. 创建 Intersection Observer 实例
const observer = new IntersectionObserver((entries) => {
    // 遍历每一个被观察的元素
    entries.forEach((entry) => {
        // 判断元素是否进入了视口
        if (entry.isIntersecting) {
            // 如果进入视口，添加 .show 类，触发 CSS 动画
            entry.target.classList.add('show');
            
            // 可选：一旦显示，就可以停止观察，以提高性能
            observer.unobserve(entry.target); 
        }
    });
}, {
    // 2. 观察者选项 (Options)
    // threshold: 元素可见度达到10%时触发回调
    threshold: 0.1 
});

// 3. 选择所有需要动画的元素
const hiddenElements = document.querySelectorAll('.hidden');

// 4. 遍历并观察每个元素
hiddenElements.forEach((el) => observer.observe(el));