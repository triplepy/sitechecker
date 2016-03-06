/**
 * Created by jelly on 3/6/16.
 */

function delete_site(){
    $("form").attr("action", "/delete");
    $("form").submit();
}