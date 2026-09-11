-- 女生宿舍员工导入
-- 生成时间: 2026-09-11 11:10:43
-- 员工数量: 44

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '雷寿燕', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '雷寿燕' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '洪学琴', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '洪学琴' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '潘珏', '天檀', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '潘珏' AND company = '天檀'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '刘佳慧 ', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '刘佳慧 ' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '江歙凤', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '江歙凤' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '孙俊', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '孙俊' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '陈倩倩', '未知', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '陈倩倩' AND company = '未知'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '冯晶琳', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '冯晶琳' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '尚歆舒', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '尚歆舒' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '刁万瑞', '未知', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '刁万瑞' AND company = '未知'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '边艳艳', '未知', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '边艳艳' AND company = '未知'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '羊蔚琛', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '羊蔚琛' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '罗国庆', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '罗国庆' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '黄明', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '黄明' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '范成杰', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '范成杰' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '何海洋', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '何海洋' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '于乐乐', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '于乐乐' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '李兴海', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '李兴海' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '杨城', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '杨城' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '包康', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '包康' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '周艳龙', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '周艳龙' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '陈清水', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '陈清水' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '茹金才', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '茹金才' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '翟飞龙', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '翟飞龙' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '张英华', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '张英华' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '姚新奥', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '姚新奥' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '方子健', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '方子健' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '李家伟', '天檀', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '李家伟' AND company = '天檀'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '马翔翔', '天檀', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '马翔翔' AND company = '天檀'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '蔡第强', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '蔡第强' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '张鹏超', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '张鹏超' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '洛绒生龙', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '洛绒生龙' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '郭红阳', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '郭红阳' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '李致远', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '李致远' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '莫红震', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '莫红震' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '李飞建', '未知', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '李飞建' AND company = '未知'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '孙晨朔', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '孙晨朔' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '刘旭', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '刘旭' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '秦孝红', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '秦孝红' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '薛健华', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '薛健华' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '庄荣飞', '拓施培', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '庄荣飞' AND company = '拓施培'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '郭雅格', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '郭雅格' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '雷志飞', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '雷志飞' AND company = '天泽'
);

INSERT INTO employees (name, company, status, created_at, updated_at)
SELECT '孙洪力', '天泽', 'active', NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM employees WHERE name = '孙洪力' AND company = '天泽'
);
